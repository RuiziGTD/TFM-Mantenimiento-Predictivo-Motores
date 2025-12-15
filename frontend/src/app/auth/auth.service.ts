import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { LoginResponse } from './login/login.model';

@Injectable({ providedIn: 'root' })
export class AuthService {

  private apiUrl = 'http://127.0.0.1:8000/login';

  constructor(private http: HttpClient) {}

  login(data: { username: string; password: string }) {
    return this.http.post<LoginResponse>(this.apiUrl, data);
  }
}
