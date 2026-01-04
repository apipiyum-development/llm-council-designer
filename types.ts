
export enum DeliberationStage {
  IDLE = 'IDLE',
  STAGE_1 = 'STAGE_1', // First Opinions
  STAGE_2 = 'STAGE_2', // Review
  STAGE_3 = 'STAGE_3'  // Final Answer
}

export interface ModelOpinion {
  id: string;
  name: string;
  color: string;
  opinion: string;
}

export interface CouncilState {
  stage: DeliberationStage;
  query: string;
  opinions: ModelOpinion[];
  reviews: ModelOpinion[];
  consensus: string;
  isLoading: boolean;
  error: string | null;
}

export interface CouncilResponse {
  opinions: { name: string; content: string }[];
  reviews: { name: string; content: string }[];
  consensus: string;
}
