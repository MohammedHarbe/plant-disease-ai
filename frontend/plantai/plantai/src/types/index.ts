export type ModelType='yolo'|'cnn';
export type AnalysisStatus='healthy'|'diseased';
export interface BoundingBox{x1:number;y1:number;x2:number;y2:number}
export interface Detection{label:string;confidence:number;status:'healthy'|'diseased';bbox?:BoundingBox;class_id?:number;class_name?:string;x?:number;y?:number;width?:number;height?:number}
export interface YoloResult{plant:string;disease:string;confidence:number;severity:string;objectsDetected:number;healthyRegions:number;diseasedRegions:number;detections:Detection[];imageUrl:string;inferenceMs:number;image_width:number;image_height:number;detection_count?:number;inference_time_ms?:number}
export interface CnnPrediction{label:string;confidence:number}
export interface CnnResult{plant:string;disease:string;confidence:number;predictions:CnnPrediction[];imageUrl:string;inferenceMs:number}
export interface HistoryItem{ id:string;plant:string;disease:string;model:ModelType;confidence:number;date:string;status:AnalysisStatus;imageUrl:string }
export interface StoredAnalysisResults{imageUrl?:string;lastModel?:ModelType;yolo?:YoloResult;cnn?:CnnResult;updatedAt?:string}
