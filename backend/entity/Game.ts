import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  ManyToMany,
  JoinTable,
} from "typeorm";

import { Genre } from "./Genre.ts";

@Entity({ name: "game" })
export class Game {
  @PrimaryGeneratedColumn()
  id!: number;

  @Column({ type: "varchar", length: 255 })
  name!: string;

  @Column({ type: "varchar", length: 255, nullable: true })
  slug?: string;

  @Column({ type: "varchar", length: 5, nullable: true })
  yearPublished?: string;

  @Column({ type: "double", nullable: true })
  bggRating?: number;

  @Column({ type: "double", nullable: true })
  difficultyRating?: number;

  // Use text if this holds more than just a short summary
  @Column({ type: "text", nullable: true })
  description?: string;

  @Column({ type: "int", nullable: true })
  playTime?: number;

  // ✅ Store as TINYINT(1) in MySQL but use boolean in TS
  @Column({ type: "bool", nullable: true })
  available?: boolean;

  @Column({ type: "int", nullable: true })
  minPlayers?: number;

  @Column({ type: "int", nullable: true })
  maxPlayers?: number;

  @ManyToMany(() => Genre, (genre) => genre.games, { eager: false })
  @JoinTable({
    name: "game_genres",
    joinColumns: [{ name: "game_id", referencedColumnName: "id" }],
    inverseJoinColumns: [{ name: "genre_id", referencedColumnName: "id" }],
  })
  genres!: Genre[];
}

