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
                name,
              } = createEvent.data;

              this.players.push(
                new Player(
                  this,
                  playerID,
                  name,
                  curr_coordinates[0],
                  curr_coordinates[1],
                  "player",
                  "player-color",
                  color
                )
              );
              console.log("Created player", playerID);
              break;
            case "move":
              const moveEvent = data as MoveEventData;
              const { id, steps_list, status, score } = moveEvent.data;
              const player = this.players.find((p) => p.id === id);
              if (!player) {
                console.log("No player found with id", id);
                return;
              }
              this.time.delayedCall(
                2000,
                () => {
                  player.followSteps(steps_list, status, score);
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

    let graphics = this.add.graphics();

    // Square settings
    let squareSize = 32; // Size of each square (32x32)
    let squaresHorizontally = 48; // Number of squares across the width
    let squaresVertically = 27; // Number of squares down the height

    graphics.lineStyle(1, 0xffffff, 0.3); // Line style: 1px wide, white, 80% opacity

    // Draw vertical lines to form squares
    for (let i = 0; i <= squaresHorizontally; i++) {
      graphics.moveTo(i * squareSize, 0);
      graphics.lineTo(i * squareSize, squaresVertically * squareSize);
    }

    // Draw horizontal lines to form squares
    for (let i = 0; i <= squaresVertically; i++) {
      graphics.moveTo(0, i * squareSize);
      graphics.lineTo(squaresHorizontally * squareSize, i * squareSize);
    }

    graphics.strokePath();

    this.players.push(
      new Player(
        this,
        1,
        "Player 1",
        0,
        0,
        "player",
        "player-color",
        "#000000",
        true
      )
    );
    this.players[0];
  }

  displayScorePopup(score: number, player: Player) {
    // Create a semi-transparent rectangle as a background
    const rect = this.add.rectangle(
      0,
      0,
      this.cameras.main.width,
      this.cameras.main.height,
      0x000000
    );
    rect.setAlpha(0.7); // Adjust alpha for transparency
    rect.setOrigin(0, 0); // Set the origin to the top-left
    rect.setDepth(1000);
    // Display the score in the center of the game screen
    const scoreText = this.add.text(
      this.cameras.main.width / 2,
      this.cameras.main.height / 2,
      `Congrats ${player.name}\nYour Score: ${score}\n\nThanks for playing!`,
      {
        fontSize: "32px",
        color: "#ffffff",
        backgroundColor: "#000000",
        padding: { left: 15, right: 15, top: 10, bottom: 10 },
      }
    );
    scoreText.setOrigin(0.5, 0.5); // Center the text's origin
    scoreText.setDepth(1001);
    player.destroy();
    this.time.delayedCall(6000, () => {
      rect.destroy();
      scoreText.destroy();
      // Refresh the window
      window.location.reload();
    });
  }
}

// Event
