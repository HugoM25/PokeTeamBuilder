import { Injectable } from '@angular/core';
import { pokeInfos } from '../models/poke-infos.model';

@Injectable({
  providedIn: 'root'
})
export class PokeInfosServiceService {

  constructor() { }

  pokelist : pokeInfos[] = [
    {id: 1, name: 'Bulbasaur', imageUrl: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png'},
    {id: 2, name: 'Charmander', imageUrl: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png'},
    {id: 3, name: 'Squirtle', imageUrl: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/7.png'},
    {id: 4, name: 'Lapras', imageUrl: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/131.png'},
    {id: 5, name: 'Gengar', imageUrl: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/94.png'},
    {id: 6, name: 'Pikachu', imageUrl: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png'}
  ];

  getPokeInfosList() {
    return this.pokelist;
  }


}
