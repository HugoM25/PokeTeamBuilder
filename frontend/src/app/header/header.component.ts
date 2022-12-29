import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent {

  constructor(private router: Router) { }

  goSettingsPage() : void {
    console.log("goSettingsPage");
  }

  goStatsPage() : void {
    console.log("goStatsPage");
    this.router.navigateByUrl('stats')
  }

  goTeamPage() : void {
    console.log("goTeamPage");
    this.router.navigateByUrl('')
  }

}
