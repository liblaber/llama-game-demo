import Phaser from "phaser";

export default class Player extends Phaser.Physics.Arcade.Sprite {
  private moveSpeed: number = 32 * 5; // pixels per second
  public id: number;
  public color: string; // Default bandana color
  public name: string;
  private bandanaSprite: Phaser.Physics.Arcade.Sprite;

  constructor(
    scene: Phaser.Scene,
    id: number,
    name: string,
    x: number,
    y: number,
    characterTexture: string | Phaser.Textures.Texture,
    bandanaTexture: string | Phaser.Textures.Texture,
    bandanaColor: string,
    ghost: boolean = false
  ) {
    super(scene, x, y, characterTexture);
    this.name = name;
    this.id = id;
    scene.add.existing(this);
    this.setOrigin(0, 0);

    // Create the bandana sprite using its texture and position it over the character
    this.bandanaSprite = new Phaser.Physics.Arcade.Sprite(
      scene,
      this.x,
      this.y,
      bandanaTexture
    );
    scene.add.existing(this.bandanaSprite);
    this.bandanaSprite.setOrigin(0, 0);

    const colorMap = {
      black: "#000000",
      white: "#ffffff",
      red: "#ff0000",
      blue: "#0000ff",
      green: "#008000",
      yellow: "#ffff00",
      orange: "#ffa500",
      purple: "#800080",
      cyan: "#00ffff",
      magenta: "#ff00ff",
      lime: "#00ff00",
      pink: "#ffc0cb",
      teal: "#008080",
      brown: "#a52a2a",
      navy: "#000080",
      maroon: "#800000",
      olive: "#808000",
      silver: "#c0c0c0",
      gold: "#ffd700",
      beige: "#f5f5dc",
      turquoise: "#40e0d0",
      indigo: "#4b0082",
      coral: "#ff7f50",
      salmon: "#fa8072",
      chocolate: "#d2691e",
    };

    // Usage:
    const normalizedColor = bandanaColor.toLowerCase();
    if (colorMap.hasOwnProperty(normalizedColor)) {
      this.color = colorMap[normalizedColor as keyof typeof colorMap];
    } else {
      // Handle unknown color
      this.color = Math.floor(Math.random() * 16777215).toString(16);
    }

    this.setColor(this.color);

    if (ghost) {
      this.setAlpha(0.5);
      this.bandanaSprite.setAlpha(0.5);
    }
  }

  followSteps(
    steps: [number, number][],
    status: "alive" | "dead",
    score: number,
    currentIndex: number = 0
  ) {
    try {
      // If there are no steps, return
      if (steps.length === 0) return;

      // Set the starting location if it's the first step
      if (currentIndex === 0) {
        const [startY, startX] = steps[0];
        this.setPosition(startX * 32, startY * 32);
        this.bandanaSprite.setPosition(startX * 32, startY * 32);
        //this.nameTag.setPosition(startX * 32 + 16, startY * 32 - 40 + 16); // Keep the nametag above the player

        // Move to the next step immediately after setting position
        this.followSteps(steps, status, score, currentIndex + 1);
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
          // After this step is complete, move to the next step
          if (currentIndex + 1 < steps.length) {
            this.followSteps(steps, status, score, currentIndex + 1);
          } else {
            // No more steps
            // Check if the player is dead
            if (status === "dead") {
              this.onDeath();
            } else {
              // @ts-ignore
              this.scene.displayScorePopup(score, this);
            }
          }
        },
      });
    } catch (err) {}
  }

  setColor(hexColor: string) {
    this.color = hexColor;
    this.bandanaSprite.setTint(parseInt(this.color.replace("#", ""), 16));
  }

  destroy(fromScene?: boolean | undefined): void {
    this.bandanaSprite.destroy();
    super.destroy(fromScene);
  }
  onDeath() {
    // Play a death animation. For this example, we'll fade the character out.
    this.scene.tweens.add({
      targets: [this, this.bandanaSprite],
      alpha: 0, // fade out
      duration: 1000, // 1 second
      ease: "Power2",
      onComplete: () => {
        // Once the animation is complete, destroy the sprites.
        this.destroy();
        this.bandanaSprite.destroy();
      },
    });
  }
}
