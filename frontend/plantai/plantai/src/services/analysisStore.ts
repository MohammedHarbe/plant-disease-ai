import type {CnnResult,ModelType,StoredAnalysisResults,YoloResult} from '../types';

const STORE_KEY='plantai:analysisResults';
const LEGACY_RESULT_KEY='plantai:lastResult';
const LEGACY_IMAGE_KEY='plantai:lastImage';

export function readStoredAnalysis():StoredAnalysisResults{
  const stored=sessionStorage.getItem(STORE_KEY);
  if(stored){
    try{return JSON.parse(stored) as StoredAnalysisResults;}catch{return {};}
  }

  const legacy=sessionStorage.getItem(LEGACY_RESULT_KEY);
  const imageUrl=sessionStorage.getItem(LEGACY_IMAGE_KEY)||undefined;
  if(!legacy)return imageUrl?{imageUrl}:{};

  try{
    const parsed=JSON.parse(legacy) as {model?:ModelType;result?:YoloResult|CnnResult};
    if(parsed.model==='yolo'&&parsed.result)return {imageUrl:imageUrl||parsed.result.imageUrl,lastModel:'yolo',yolo:parsed.result as YoloResult};
    if(parsed.model==='cnn'&&parsed.result)return {imageUrl:imageUrl||parsed.result.imageUrl,lastModel:'cnn',cnn:parsed.result as CnnResult};
  }catch{
    return imageUrl?{imageUrl}:{};
  }

  return imageUrl?{imageUrl}:{};
}

export function saveAnalysisImage(imageUrl:string):void{
  const current=readStoredAnalysis();
  const next:StoredAnalysisResults={...current,imageUrl,updatedAt:new Date().toISOString()};
  sessionStorage.setItem(STORE_KEY,JSON.stringify(next));
  sessionStorage.setItem(LEGACY_IMAGE_KEY,imageUrl);
}

export function saveAnalysisResult(model:'yolo',result:YoloResult,imageUrl?:string):void;
export function saveAnalysisResult(model:'cnn',result:CnnResult,imageUrl?:string):void;
export function saveAnalysisResult(model:ModelType,result:YoloResult|CnnResult,imageUrl?:string):void{
  const current=readStoredAnalysis();
  const next:StoredAnalysisResults={
    ...current,
    imageUrl:imageUrl||current.imageUrl||result.imageUrl,
    lastModel:model,
    updatedAt:new Date().toISOString(),
    ...(model==='yolo'?{yolo:result as YoloResult}:{cnn:result as CnnResult}),
  };
  sessionStorage.setItem(STORE_KEY,JSON.stringify(next));
  sessionStorage.setItem(LEGACY_RESULT_KEY,JSON.stringify({model,result}));
  if(next.imageUrl)sessionStorage.setItem(LEGACY_IMAGE_KEY,next.imageUrl);
}
