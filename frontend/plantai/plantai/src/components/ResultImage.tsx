import {useEffect,useMemo,useRef,useState} from 'react';
import type {CSSProperties} from 'react';
import type {Detection} from '../types';

type ImageSize={width:number;height:number};
const MAX_UPSCALE=2.5;

function boxStyle(detection:Detection,imageSize:ImageSize|undefined):CSSProperties{
  if(detection.bbox&&imageSize?.width&&imageSize.height){
    const x1=Math.max(0,Math.min(imageSize.width,detection.bbox.x1));
    const y1=Math.max(0,Math.min(imageSize.height,detection.bbox.y1));
    const x2=Math.max(x1,Math.min(imageSize.width,detection.bbox.x2));
    const y2=Math.max(y1,Math.min(imageSize.height,detection.bbox.y2));

    return {
      left:`${(x1/imageSize.width)*100}%`,
      top:`${(y1/imageSize.height)*100}%`,
      width:`${((x2-x1)/imageSize.width)*100}%`,
      height:`${((y2-y1)/imageSize.height)*100}%`,
    };
  }

  return {
    left:`${detection.x??0}%`,
    top:`${detection.y??0}%`,
    width:`${detection.width??0}%`,
    height:`${detection.height??0}%`,
  };
}

function fitImage(source:ImageSize|undefined,container:ImageSize|undefined):ImageSize|undefined{
  if(!source?.width||!source.height||!container?.width||!container.height)return undefined;

  const fitScale=Math.min(container.width/source.width,container.height/source.height);
  const scale=fitScale>1?Math.min(fitScale,MAX_UPSCALE):fitScale;

  return {
    width:Math.max(1,Math.round(source.width*scale)),
    height:Math.max(1,Math.round(source.height*scale)),
  };
}

export default function ResultImage({
  imageUrl,
  detections,
  imageWidth,
  imageHeight,
}:{imageUrl:string;detections:Detection[];imageWidth?:number;imageHeight?:number}){
  const containerRef=useRef<HTMLDivElement|null>(null);
  const [containerSize,setContainerSize]=useState<ImageSize|undefined>();
  const [naturalSize,setNaturalSize]=useState<ImageSize|undefined>(
    imageWidth&&imageHeight?{width:imageWidth,height:imageHeight}:undefined,
  );
  const size=naturalSize||(imageWidth&&imageHeight?{width:imageWidth,height:imageHeight}:undefined);
  const fittedSize=useMemo(()=>fitImage(size,containerSize),[size,containerSize]);

  useEffect(()=>{
    const element=containerRef.current;
    if(!element)return;

    const updateSize=()=>setContainerSize({width:element.clientWidth,height:element.clientHeight});
    updateSize();

    const observer=new ResizeObserver(updateSize);
    observer.observe(element);

    return ()=>observer.disconnect();
  },[]);

  return <div ref={containerRef} className="relative flex h-[380px] w-full items-center justify-center overflow-hidden rounded-[28px] bg-[#f5f7f2] md:h-[400px]">
    <div
      className="relative max-h-full max-w-full"
      style={fittedSize?{width:fittedSize.width,height:fittedSize.height}:undefined}
    >
      <img
        src={imageUrl}
        alt="Analyzed plant"
        onLoad={event=>{
          const image=event.currentTarget;
          if(image.naturalWidth&&image.naturalHeight){
            setNaturalSize({width:image.naturalWidth,height:image.naturalHeight});
          }
        }}
        className="block h-full w-full object-contain object-center"
      />
      {detections.map((detection,index)=><div
        key={`${detection.class_name||detection.label}-${index}`}
        className={`absolute rounded-xl border-2 ${detection.status==='diseased'?'border-[#ef9a78]':'border-[#9ce38b]'}`}
        style={boxStyle(detection,size)}
      >
        <span className={`absolute left-1 top-1 max-w-[calc(100vw-4rem)] truncate rounded-lg px-2.5 py-1 text-[10px] font-bold text-white shadow-sm ${detection.status==='diseased'?'bg-[#b9573a]':'bg-[#3e7c4a]'}`}>
          {detection.label} · {Math.round(detection.confidence*100)}%
        </span>
      </div>)}
      <div className="absolute bottom-4 left-4 rounded-full bg-[#173b27]/90 px-3 py-1.5 text-xs font-bold text-white backdrop-blur">Live detection overlay</div>
    </div>
  </div>;
}
