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

  @ViewChild('healthChart')
  chartRef!: ElementRef<HTMLCanvasElement>;

  constructor(private http: HttpClient, private cd: ChangeDetectorRef) {}

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

          // 🔹 Fuerza que Angular detecte los cambios inmediatamente
          this.cd.detectChanges();

          // 🔹 Crear el gráfico después de que Angular haya actualizado la vista
          this.createHealthChart();
        },
        error: err => console.error(err)
      });
  }

  createHealthChart() {
    if (!this.result?.dashboard?.overview) return;

    const overview = this.result.dashboard.overview;

    // Si ya existe, destruye el gráfico
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
          backgroundColor: ['#10b981', '#facc15', '#ef4444']
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true, ticks: { precision: 0 } } }
      }
    });
  }
}
