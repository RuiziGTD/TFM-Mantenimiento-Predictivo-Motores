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

  searchText: string = '';
  statusFilter: string = 'ALL';
  sortDirection: 'asc' | 'desc' = 'asc';
  filteredTableMotors: any[] = [];

  topCriticalMotorsList: any[] = []; // panel 3: top 5 críticos únicos

  @ViewChild('healthChart') chartRef!: ElementRef<HTMLCanvasElement>;

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

          // Paneles iniciales
          this.selectedStatus = null;
          this.filteredMotors = [];

          // Panel 4: tabla completa
          this.filteredTableMotors = [...this.result.dashboard.units];

          // Panel 3: top 5 críticos únicos
          this.topCriticalMotorsList = this.computeTopCriticalMotors();

          this.cd.detectChanges(); // fuerza actualización
          this.createHealthChart();
        },
        error: err => console.error(err)
      });
  }

  createHealthChart() {
    if (!this.result) return;

    const overview = this.result.dashboard.overview;

    if (this.chart) this.chart.destroy();

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
        scales: { y: { beginAtZero: true, ticks: { precision: 0 } } },
        onClick: (evt, elements) => {
          if (!elements.length) return;
          const index = elements[0].index;
          const statusMap = ['OK', 'AVISO', 'CRITICO'];
          this.selectedStatus = statusMap[index];
          this.filterMotorsByStatus(this.selectedStatus);
          this.cd.detectChanges();
        }
      }
    });
  }

  filterMotorsByStatus(status: string) {
    if (!this.result?.dashboard?.units) return;

    const seen = new Set<number>();
    this.filteredMotors = this.result.dashboard.units.reduce((acc: any[], u: any) => {
      if (u.status.toUpperCase() === status.toUpperCase() && !seen.has(u.unit_id)) {
        acc.push(u);
        seen.add(u.unit_id);
      }
      return acc;
    }, []);
  }

  applyTableFilters() {
    if (!this.result || !this.result.dashboard?.units) return;

    const units: any[] = this.result.dashboard.units;

    this.filteredTableMotors = units.filter((m: any) => {
      const matchesSearch = m.unit_id?.toString().includes(this.searchText ?? '');
      const matchesStatus = this.statusFilter === 'ALL' || (m.status?.toUpperCase() === this.statusFilter);
      return matchesSearch && matchesStatus;
    });

    this.sortTable();
  }

  toggleSort() {
    this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
    this.sortTable();
  }

  sortTable() {
    this.filteredTableMotors.sort((a, b) =>
      this.sortDirection === 'asc' ? a.rul - b.rul : b.rul - a.rul
    );
  }

  private computeTopCriticalMotors(): any[] {
    if (!this.result) return [];
    const uniqueUnits: { [key: number]: any } = {};

    // Mantenemos el motor con menor RUL por unit_id
    for (const u of this.result.dashboard.units) {
      const existing = uniqueUnits[u.unit_id];
      if (!existing || u.rul < existing.rul) uniqueUnits[u.unit_id] = u;
    }

    // Top 5 críticos
    return Object.values(uniqueUnits)
      .filter(u => u.status.toUpperCase() === 'CRITICO')
      .sort((a, b) => a.rul - b.rul)
      .slice(0, 5);
  }
}
