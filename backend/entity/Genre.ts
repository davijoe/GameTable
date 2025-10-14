import { Entity, PrimaryGeneratedColumn, Column, ManyToMany } from "typeorm";
import { Game } from "./Game.ts";

@Entity({ name: "genre" })
export class Genre {
  @PrimaryGeneratedColumn({ type: "int", name: "id" })
  id!: number;

  @Column("varchar", { name: "title", length: 30 })
  title!: string;

  @Column("varchar", { name: "description", length: 255, nullable: true })
  description!: string | null;

  @ManyToMany(() => Game, (g) => g.genres)
  games!: Game[];
}
