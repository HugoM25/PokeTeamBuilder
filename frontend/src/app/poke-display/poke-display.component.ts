import { Component } from '@angular/core';
import { pokeInfos } from '../models/poke-infos.model';
import { PokeInfosServiceService } from '../services/poke-infos-service.service';
import { OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-poke-display',
  templateUrl: './poke-display.component.html',
  styleUrls: ['./poke-display.component.scss']
})
export class PokeDisplayComponent implements OnInit {
  @Input() pokeInfos!: pokeInfos; 

  constructor(private pokeInfosService: PokeInfosServiceService) { }

  ngOnInit(): void {
    this.pokeInfos = this.pokeInfosService.getPokeInfosList()[0];
  }
}
