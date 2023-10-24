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
    bandanaColor: string
  ) {
    super(scene, x, y, characterTexture);
    this.name = name;
    this.x += 16;
    this.y += 16;
    this.id = id;
    scene.add.existing(this);
    this.setScale(1.5);

    // Create the bandana sprite using its texture and position it over the character
    this.bandanaSprite = new Phaser.Physics.Arcade.Sprite(
      scene,
      this.x,
      this.y,
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
