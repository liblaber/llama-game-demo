import Phaser from "phaser";

export default class Player extends Phaser.Physics.Arcade.Sprite {
  private moveSpeed: number = 32 * 5; // pixels per second
  public id: number;
  public color: string; // Default bandana color
  public name: string;
  private bandanaSprite: Phaser.Physics.Arcade.Sprite;
  private nameTag: Phaser.GameObjects.Text; // The nametag

  constructor(
    scene: Phaser.Scene,
    id: number,
    x: number,
    y: number,
    characterTexture: string | Phaser.Textures.Texture,
    bandanaTexture: string | Phaser.Textures.Texture,
    playerName: string, // Player's name for the nametag
    bandanaColor: string
  ) {
    super(scene, x, y, characterTexture);
    this.id = id;
    scene.add.existing(this);
    this.setScale(1.5);

    // Create the bandana sprite using its texture and position it over the character
    this.bandanaSprite = new Phaser.Physics.Arcade.Sprite(
      scene,
      x,
      y,
      bandanaTexture
    );
    scene.add.existing(this.bandanaSprite);
    this.bandanaSprite.setScale(1.5);

    this.color = Math.floor(Math.random() * 16777215).toString(16);
    if (bandanaColor.toLowerCase() == "black") {
      this.color = "#000000";
    }

    if (bandanaColor.toLowerCase() == "white") {
      this.color = "#ffffff";
    }

    this.setColor(this.color);

    // Create the nametag
    this.name = playerName;
    this.nameTag = scene.add
      .text(x, y - 40, this.name, {
        fontSize: "20px",
        color: "#fff",
        backgroundColor: "#000",
        padding: { left: 5, right: 5, top: 2, bottom: 2 }, // Some padding around the text
      })
      .setOrigin(0.5, 0.5); // Center the text's origin
  }

  followSteps(steps: [number, number][], currentIndex: number = 0) {
    // If there are no steps, return
    if (steps.length === 0) return;

    // Set the starting location if it's the first step
    if (currentIndex === 0) {
      const [startY, startX] = steps[0];
      this.setPosition(startX * 32, startY * 32);
      this.bandanaSprite.setPosition(startX * 32, startY * 32);
      this.nameTag.setPosition(startX * 32, startY * 32 - 40); // Keep the nametag above the player

      // Move to the next step immediately after setting position
      this.followSteps(steps, currentIndex + 1);
      return;
    }

    const [dy, dx] = steps[currentIndex];
    const newX = this.x + dx * 32; // Multiply by 32 for actual pixel offset
    const newY = this.y + dy * 32; // Multiply by 32 for actual pixel offset

    const distance = Math.sqrt(dx * dx + dy * dy) * 32; // Multiply by 32 for actual pixel distance
    const duration = (distance / this.moveSpeed) * 1000;

    // Move the player and bandana
    this.scene.tweens.add({
      targets: [this, this.bandanaSprite],
      x: newX,
      y: newY,
      duration: duration,
      ease: "Power2",
      onComplete: () => {
        // Move the nametag along with the player
        this.scene.tweens.add({
          targets: this.nameTag,
          x: newX,
          y: newY - 40, // Keep the nametag above the player
          duration: duration,
          ease: "Power2",
          onComplete: () => {
            // After this step is complete, move to the next step
            this.followSteps(steps, currentIndex + 1);
          },
        });
      },
    });
  }

  setColor(hexColor: string) {
    this.color = hexColor;
    this.bandanaSprite.setTint(parseInt(this.color.replace("#", ""), 16));
  }
}
