import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common'; // ← Import necesario
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, CommonModule], // ← Añadir CommonModule
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  username = '';
  password = '';
  message = '';

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}


  onSubmit() {
    this.authService.login({
      username: this.username,
      password: this.password
    }).subscribe({
      next: (res) => {
        if (res.access_token) {
          localStorage.setItem('token', res.access_token);
          this.router.navigate(['/home']);
        }
        this.message = res.message;
      },
      error: (err) => {
        if (err.status === 422) {
          this.message = 'Usuario y contraseña no pueden estar vacíos';
        } else {
          this.message = err.error?.detail || 'Credenciales incorrectas';
        }
      }
    });
  }
}
