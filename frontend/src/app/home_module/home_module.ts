import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { HomeComponent } from './home/home';

@NgModule({
//  declarations: [HomeComponent],
  imports: [
    CommonModule,
    FormsModule,
    HttpClientModule
  ]
})
export class HomeModule {}