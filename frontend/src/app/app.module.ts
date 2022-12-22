import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { PokeDisplayComponent } from './poke-display/poke-display.component';
import { HttpClientModule } from '@angular/common/http';
import { HeaderComponent } from './header/header.component';
import { CommandsElementsComponent } from './commands-elements/commands-elements.component';
import { TeamPageComponent } from './team-page/team-page.component';

@NgModule({
  declarations: [
    AppComponent,
    PokeDisplayComponent,
    HeaderComponent,
    CommandsElementsComponent,
    TeamPageComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
