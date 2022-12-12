import { Injectable } from '@angular/core';
import { pokeInfos } from '../models/poke-infos.model';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class PokeInfosServiceService {

  constructor(private http:HttpClient) { }

  pokeNames : string[] = [
    'Bulbasaur',
    'Charmander',
    'Squirtle',
    'Lapras',
    'Gengar',
    'Pikachu'
  ]

  //Get the list of pokeInfos from the backend
  getPokeInfosList() : Observable<pokeInfos[]> {
    return this.http.get<pokeInfos[]>('http://127.0.0.1:5000');
  }

  getPokeNames():string[] {
    return this.pokeNames;
  }


}
