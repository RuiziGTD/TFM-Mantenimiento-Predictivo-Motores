import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [FormsModule, HttpClientModule], 
  templateUrl: './home.html',   
  styleUrls: ['./home.css']     
})
export class HomeComponent {
  selectedFile?: File;
  result: any;

  constructor(private http: HttpClient) {}

  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
  }

  predict() {
    if (!this.selectedFile) return;

    const formData = new FormData();
    formData.append('file', this.selectedFile);

    this.http.post('http://localhost:8000/predict', formData)
      .subscribe(res => this.result = res,
                 err => console.error(err));
  }
}
