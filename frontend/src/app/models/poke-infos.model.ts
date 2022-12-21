import { Input } from "@angular/core";

export class pokeInfos {
    id!: number;
    name!: string; 
    imageUrl!: string;
    isLocked!: boolean;

    constructor(name: string, imageUrl: string, isLocked: boolean) {
        this.name = name;
        this.imageUrl = imageUrl;
    }
}