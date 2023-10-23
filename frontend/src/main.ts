import Phaser from "phaser";

import MainScene from "./MainScene";

const config: Phaser.Types.Core.GameConfig = {
  type: Phaser.AUTO,
  parent: "app",
  width: 1504,
  height: 832,
  scene: [MainScene],
};

export default new Phaser.Game(config);
