
export class PokeInfos {
    id!: number;
    name!: string; 
    imageUrl!: string;
    isLocked!: boolean;

    constructor(name: string, imageUrl: string, isLocked: boolean) {
        this.name = name;
        this.imageUrl = imageUrl;
    }
}