interface IEventData {
  event: string;
  data: Record<string, any>;
}

export interface CreateEventData extends IEventData {
  data: {
    name: string;
    color: string;
    id: number;
    score: number;
    start_coordinates: [number, number];
    curr_coordinates: [number, number];
    steps_list: [number, number][];
    status: string;
  };
}

export interface StepEventData extends IEventData {
  data: {
    id: number;
    direction: string;
    steps: number;
  };
}

export interface MoveEventData extends IEventData {
  data: {
    name: string;
    color: string;
    id: number;
    score: number;
    start_coordinates: [number, number];
    curr_coordinates: [number, number];
    steps_list: [number, number][];
    status: "alive" | "dead";
  };
}
