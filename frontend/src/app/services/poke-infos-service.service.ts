import { Injectable } from '@angular/core';
import { pokeInfos } from '../models/poke-infos.model';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class PokeInfosServiceService {

  constructor(private http:HttpClient) { }

  pokeNames : string[] = [
    'bulbasaur',
    'charmander',
    'squirtle',
    'lapras',
    'gengar',
    'pikachu'
  ]

  //Get the list of pokeInfos from the backend
  getPokeInfosList() : Observable<pokeInfos[]> {
    return this.http.get<pokeInfos[]>('http://127.0.0.1:5000');
  }

  getPokeData(pokeName: string) : Observable<pokeInfos> {
    const body = { name: pokeName };
    const req = this.http.post<pokeInfos>('http://127.0.0.1:5000/set_pkm', body);
    req.subscribe();
    return req;
  }

  getPokeNames():Observable<string[]> {
    return this.http.get<string[]>('http://127.0.0.1:5000/pkm_list');
  }


}
