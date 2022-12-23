import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TeamPageComponent } from './team-page/team-page.component';
import { StatsPageComponent } from './stats-page/stats-page.component';

const routes: Routes = [
  { path: '', component: TeamPageComponent },
  { path: 'stats', component : StatsPageComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
