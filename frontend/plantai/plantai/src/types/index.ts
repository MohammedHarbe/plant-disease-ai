export type ModelType='yolo'|'cnn';
export type AnalysisStatus='healthy'|'diseased';
export interface Detection{label:string;confidence:number;x:number;y:number;width:number;height:number;status:'healthy'|'diseased'}
export interface YoloResult{plant:string;disease:string;confidence:number;severity:string;objectsDetected:number;healthyRegions:number;diseasedRegions:number;detections:Detection[];imageUrl:string;inferenceMs:number}
export interface CnnPrediction{label:string;confidence:number}
export interface CnnResult{plant:string;disease:string;confidence:number;predictions:CnnPrediction[];imageUrl:string;inferenceMs:number}
export interface HistoryItem{ id:string;plant:string;disease:string;model:ModelType;confidence:number;date:string;status:AnalysisStatus;imageUrl:string }
