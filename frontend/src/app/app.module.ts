import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { PokeDisplayComponent } from './poke-display/poke-display.component';
import { PokeDisplayListComponent } from './poke-display-list/poke-display-list.component';

@NgModule({
  declarations: [
    AppComponent,
    PokeDisplayComponent,
    PokeDisplayListComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
