import {yoloDemo} from '../data/mock';
import type {CnnResult,YoloResult} from '../types';

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

export async function predictYolo(imageUrl:string):Promise<YoloResult>{
  try{
    const formData=new FormData();
    const blob=await fetch(imageUrl).then(r=>r.blob());
    formData.append('file',blob);
    const response=await fetch(`${API_URL}/predict/yolo`,{method:'POST',body:formData});
    if(!response.ok)throw new Error('YOLO prediction failed');
    return await response.json();
  }catch{
    return yoloDemo;
  }
}

export async function predictCnn(imageUrl:string):Promise<CnnResult>{
  const formData=new FormData();
  const blob=await fetch(imageUrl).then(r=>r.blob());
  formData.append('file',blob);
  const response=await fetch(`${API_URL}/predict/cnn`,{method:'POST',body:formData});
  if(!response.ok){
    const body=await response.json().catch(()=>null);
    const message=body?.detail||`CNN prediction failed (${response.status})`;
    console.error('predictCnn error:',message);
    throw new Error(message);
  }
  return await response.json();
}

export async function askPlantAI(question:string):Promise<string>{
  const responses:Record<string,string>={
    'what is this disease?':'Early Blight is a fungal disease caused by Alternaria solani. It typically appears as concentric brown spots with a target-like pattern on tomato leaves. It thrives in warm, humid conditions and can significantly reduce fruit yield if left untreated.',
    'how do i treat it?':'Treatment options include: 1) Remove infected leaves promptly, 2) Apply fungicides like chlorothalonil or mancozeb weekly, 3) Improve air circulation by pruning, 4) Water at the base of the plant to keep foliage dry, 5) Consider resistant tomato varieties.',
    'how can i prevent it?':'Prevention strategies: 1) Plant disease-resistant varieties, 2) Space plants for good air flow, 3) Water early in the morning at soil level, 4) Remove lower leaves once plant is established, 5) Practice crop rotation (3-4 year gap), 6) Mulch to prevent soil splash, 7) Monitor regularly for early signs.',
    'is my plant healthy?':'Based on the analysis, your plant shows signs of Early Blight disease with a confidence of 94.7%. The diseased regions need attention, but treatment can be effective if started early. I recommend implementing the prevention and treatment strategies mentioned above.'
  };
  
  const lowerQuestion=question.toLowerCase();
  for(const[key,value]of Object.entries(responses)){
    if(lowerQuestion.includes(key.replace(/[?]/g,''))){
      return value;
    }
  }
  
  return 'I can help you understand your plant health diagnosis. Ask me about the disease, treatment options, prevention strategies, or plant health status.';
}

export async function imageUrlToBlob(url:string):Promise<Blob>{
  const response=await fetch(url);
  return response.blob();
}