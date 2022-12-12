import { Component } from '@angular/core';
import { pokeInfos } from '../models/poke-infos.model';
import { PokeInfosServiceService } from '../services/poke-infos-service.service';
import { OnInit } from '@angular/core';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-poke-display-list',
  templateUrl: './poke-display-list.component.html',
  styleUrls: ['./poke-display-list.component.scss']
})
export class PokeDisplayListComponent implements OnInit{

  pokeInfosList$!: Observable<pokeInfos[]>;

  constructor(private pokeInfosService: PokeInfosServiceService) { }

  ngOnInit(): void {
    this.pokeInfosList$ = this.pokeInfosService.getPokeInfosList();
    console.log(this.pokeInfosList$);
  }
  //Change the pokemon at the emplacement
  changePoke(newName:string){
    alert(newName);

  }
}
