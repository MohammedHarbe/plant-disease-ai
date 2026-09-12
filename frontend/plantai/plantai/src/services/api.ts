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

export async function askPlantAI(question:string,context?:Record<string,unknown>):Promise<string>{
  const response=await fetch(`${API_URL}/chat`,{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({message:question,context}),
  });
  const body=await response.json().catch(()=>null);
  if(!response.ok){
    throw new Error(body?.detail||`Chat request failed (${response.status})`);
  }
  if(typeof body?.response!=='string'){
    throw new Error('The chat service returned an invalid response.');
  }
  return body.response;
}

export async function imageUrlToBlob(url:string):Promise<Blob>{
  const response=await fetch(url);
  return response.blob();
}