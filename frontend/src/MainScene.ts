import Phaser from "phaser";
import Player from "./Player";
import { CreateEventData, MoveEventData } from "./interfaces";

export default class MainScene extends Phaser.Scene {
  private players: Player[] = [];
  constructor() {
    super("hello-world");
  }

  preload() {
    this.load.image("tiles", "tilesets/sprite_sheet.png");
    this.load.tilemapTiledJSON("map", "tilemaps/map.tmj");
    this.load.image("player", "alpaca_front_base.png");
    this.load.image("player-color", "alpaca_front_color.png");
  }

  create() {
    const socket = new WebSocket("ws://localhost:8000/ws/1");
    socket.onopen = () => {
      console.log("Connected to server");
    };
    socket.onmessage = (event: MessageEvent) => {
      try {
        // Assuming server sends a JSON payload
        const data = JSON.parse(event.data);
        console.log("Received data:", data);

        // Check if their is a event key
        if (data.event && data.data) {
          switch (data.event) {
            case "create":
              const createEvent = data as CreateEventData;
              const {
                id: playerID,
                color,
                curr_coordinates,
              } = createEvent.data;

              this.players.push(
                new Player(
                  this,
                  playerID,
                  curr_coordinates[0] * 32,
                  curr_coordinates[1] * 32,
                  "player",
                  "player-color",
                  color
                )
              );
              console.log("Created player", playerID);
              break;
            case "move":
              const moveEvent = data as MoveEventData;
              const { id, steps_list } = moveEvent.data;
              const player = this.players.find((p) => p.id === id);
              if (!player) {
                console.log("No player found with id", id);
                return;
              }
              this.time.delayedCall(
                2000,
                () => {
                  player.followSteps(steps_list);
                },
                [],
                this
              );
              console.log("Moved player", id);
              break;
          }
        }
        console.log(data);
      } catch (err) {
        console.log(event);
        console.error("Error parsing JSON payload:", err);
      }
    };

    const map = this.make.tilemap({ key: "map" });

    const tileset = map.addTilesetImage("PokemonTiles", "tiles");

    const below = map.createLayer("Below Player", tileset, 0, 0);
    below.setDepth(-1);
    const floor = map.createLayer("Map", tileset, 0, 0);
    floor.setDepth(1);
    const decoration = map.createLayer("Decoration", tileset, 0, 0);
    decoration.setDepth(2);
    const above = map.createLayer("Above Player", tileset, 0, 0);
    above.setDepth(10);
    // this.players.push(
    //   new Player(
    //     this,
    //     32 * 5,
    //     32 * 5,
    //     "player",
    //     "player-color",
    //     "Llama Joe",
    //     Math.floor(Math.random() * 16777215).toString(16)
    //   )
    // );
  }

  async wait(durationInMilliseconds: number) {
    return new Promise((resolve) => {
      this.time.delayedCall(durationInMilliseconds, resolve);
    });
  }
}

// Event
