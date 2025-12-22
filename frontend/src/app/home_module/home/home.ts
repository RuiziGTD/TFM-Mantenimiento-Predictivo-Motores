import { Component, ViewChild, ElementRef, ChangeDetectorRef } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { Chart } from 'chart.js/auto';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [FormsModule, HttpClientModule, CommonModule],
  templateUrl: './home.html',
  styleUrls: ['./home.css']
})
export class HomeComponent {

  selectedFile?: File;
  result: any;

  chart: Chart | undefined;

  filteredMotors: any[] = [];
  selectedStatus: string | null = null;

  @ViewChild('healthChart') chartRef!: ElementRef<HTMLCanvasElement>;

  constructor(private http: HttpClient, private cd: ChangeDetectorRef) {} // ← Injectamos ChangeDetectorRef

  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
  }

  predict() {
    if (!this.selectedFile) return;

    const formData = new FormData();
    formData.append('file', this.selectedFile);

    this.http.post('http://localhost:8000/predict', formData)
      .subscribe({
        next: (res: any) => {
          this.result = res;

          // Forzamos repaint y detección de cambios
          this.cd.detectChanges();

          this.createHealthChart();
        },
        error: err => console.error(err)
      });
  }

  createHealthChart() {
    const overview = this.result.dashboard.overview;

    if (this.chart) {
      this.chart.destroy();
    }

    this.chart = new Chart(this.chartRef.nativeElement, {
      type: 'bar',
      data: {
        labels: ['OK', 'AVISO', 'CRÍTICO'],
        datasets: [{
          label: 'Motores',
          data: [
            overview.ok_units,
            overview.warning_units,
            overview.critical_units
          ],
          backgroundColor: ['#16a34a', '#facc15', '#dc2626']
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
          y: { beginAtZero: true, ticks: { precision: 0 } }
        },
        onClick: (evt, elements) => {
          if (!elements.length) return;
          const index = elements[0].index;
          const statusMap = ['OK', 'AVISO', 'CRITICO'];
          this.selectedStatus = statusMap[index];
          this.filterMotorsByStatus(this.selectedStatus);
          this.cd.detectChanges(); // ← Fuerza actualización
        }
      }
    });
  }

  filterMotorsByStatus(status: string) {
    this.filteredMotors = this.result.dashboard.units.filter((u: any) => u.status.toUpperCase() === status);
  }
}
