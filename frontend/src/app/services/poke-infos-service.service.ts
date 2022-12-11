import { Injectable } from '@angular/core';
import { pokeInfos } from '../models/poke-infos.model';

@Injectable({
  providedIn: 'root'
})
export class PokeInfosServiceService {

  constructor() { }

  pokelist : pokeInfos[] = [
    {id: 1, name: 'Bulbasaur', imageUrl: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png'}
  ];

  getPokeInfosList() {
    return this.pokelist;
  }


}
