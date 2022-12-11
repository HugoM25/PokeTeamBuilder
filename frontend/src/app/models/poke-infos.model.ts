import { Input } from "@angular/core";

export class pokeInfos {
    id!: number;
    name!: string; 
    description!: string;
    imageUrl!: Date;

    constructor(name: string, imageUrl: string) {
    }

}