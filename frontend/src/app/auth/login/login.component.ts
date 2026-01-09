import { Component, ChangeDetectorRef } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  username = '';
  password = '';
  message = '';

  constructor(
    private authService: AuthService,
    private router: Router,
    private cd: ChangeDetectorRef
  ) {}

  onSubmit() {
    this.authService.login({
      username: this.username || '',
      password: this.password || ''
    }).subscribe({
      next: (res) => {
        if (res.access_token) {
          localStorage.setItem('token', res.access_token);
          this.router.navigate(['/home']);
        }
        this.message = res.message;
        this.cd.detectChanges(); // ← fuerza repaint
      },
      error: (err) => {
        if (err.error) {
          // Si es un array de errores de Pydantic
          if (Array.isArray(err.error)) {
            this.message = err.error.map((e: any) => e.msg).join(', ');
          } 
          // Si FastAPI envía un objeto con "detail"
          else if (typeof err.error.detail === 'string') {
            this.message = err.error.detail;
          } 
          else if (Array.isArray(err.error.detail)) {
            // Pydantic dentro de "detail"
            this.message = err.error.detail.map((e: any) => e.msg).join(', ');
          } 
          else {
            this.message = JSON.stringify(err.error);
          }
        } else {
          this.message = 'Credenciales incorrectas';
        }
        this.cd.detectChanges();
      }
    });
  }
}
