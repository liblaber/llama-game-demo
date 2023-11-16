import Phaser from "phaser";

export default class Player extends Phaser.Physics.Arcade.Sprite {
  private moveSpeed: number = 32 * 5; // pixels per second
  public llama_id: number;
  public color: string; // Default bandana color
  public name: string;
  private bandanaSprite: Phaser.Physics.Arcade.Sprite;

  constructor(
    scene: Phaser.Scene,
    llama_id: number,
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
    this.llama_id = llama_id;
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
      if (currentIndex >= steps.length) {
        // If we've processed all steps, check status and display score
        this.checkStatusAndDisplayScore(status, score);
        return;
      }

      // Get the current step from the array
      const [dy, dx] = steps[currentIndex];
      const newX = this.x + dx * 32; // 32 is the size of a tile in pixels
      const newY = this.y + dy * 32;

      const distance = Math.sqrt(dx * dx + dy * dy) * 32; // Calculate the distance for the current step
      const duration = (distance / this.moveSpeed) * 1000; // Calculate the duration for the tween animation

      // Animate the player's movement
      this.scene.tweens.add({
        targets: [this, this.bandanaSprite],
        x: newX,
        y: newY,
        duration: duration,
        ease: "Power2",
        onComplete: () => {
          // After completing the current step, process the next step
          this.followSteps(steps, status, score, currentIndex + 1);
        },
      });
    } catch (err) {
      console.error("Error in followSteps:", err);
      this.checkStatusAndDisplayScore(status, score);
    }
  }

  private checkStatusAndDisplayScore(status: "alive" | "dead", score: number) {
    // @ts-ignore
    this.scene.displayScorePopup(score, this, status === "dead");
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
