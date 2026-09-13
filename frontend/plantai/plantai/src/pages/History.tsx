import {useMemo,useState} from 'react';
import {CalendarDays,ChevronRight,Filter,Leaf} from 'lucide-react';
import {Link} from 'react-router-dom';
import {readStoredAnalysis} from '../services/analysisStore';
import type {CnnResult,HistoryItem,ModelType,YoloResult} from '../types';

function statusFor(result:YoloResult|CnnResult):'healthy'|'diseased'{
  return result.disease.toLowerCase().includes('healthy')?'healthy':'diseased';
}

function formatDate(value?:string):string{
  if(!value)return 'Current session';
  const date=new Date(value);
  if(Number.isNaN(date.getTime()))return 'Current session';
  return date.toLocaleString(undefined,{month:'short',day:'numeric',hour:'numeric',minute:'2-digit'});
}

function toHistoryItem(model:ModelType,result:YoloResult|CnnResult,updatedAt?:string):HistoryItem{
  return {
    id:`current-${model}`,
    plant:result.plant,
    disease:result.disease,
    model,
    confidence:result.confidence,
    date:formatDate(updatedAt),
    status:statusFor(result),
    imageUrl:result.imageUrl,
  };
}

export default function History(){
  const [filter,setFilter]=useState<'all'|ModelType|'healthy'|'diseased'>('all');
  const stored=readStoredAnalysis();
  const allItems=useMemo(()=>[
    ...(stored.yolo?[toHistoryItem('yolo',stored.yolo,stored.updatedAt)]:[]),
    ...(stored.cnn?[toHistoryItem('cnn',stored.cnn,stored.updatedAt)]:[]),
  ],[stored.cnn,stored.updatedAt,stored.yolo]);
  const items=useMemo(()=>allItems.filter(item=>filter==='all'||item.model===filter||item.status===filter),[allItems,filter]);

  return <div className="p-5 lg:p-9"><div className="flex flex-wrap items-end justify-between gap-4"><div><div className="pill border-[#dbe8d6] bg-white text-[#58775d]"><CalendarDays size={13}/>Scan archive</div><h1 className="mt-4 font-display text-3xl font-extrabold">Analysis history</h1><p className="mt-2 text-sm text-[#7b887f]">Review plant health scans saved in this browser session.</p></div><div className="flex flex-wrap gap-2">{(['all','yolo','cnn','healthy','diseased'] as const).map(f=><button key={f} onClick={()=>setFilter(f)} className={`rounded-full px-3.5 py-2 text-xs font-bold capitalize transition ${filter===f?'bg-[#173b27] text-white':'border border-[#dce6d9] bg-white text-[#637268] hover:bg-[#f5f8f2]'}`}><Filter size={12} className="mr-1 inline"/>{f}</button>)}</div></div><div className="mt-6 card overflow-hidden"><div className="hidden grid-cols-[1.8fr_1fr_1fr_.7fr_.9fr] gap-4 border-b border-[#e9eee6] bg-[#fafbf8] px-6 py-4 text-[10px] font-bold uppercase tracking-widest text-[#879188] md:grid"><div>Plant</div><div>Model</div><div>Result</div><div>Confidence</div><div>Date</div></div>{items.length?items.map(item=><Link to={item.model==='yolo'?'/results/yolo':'/results/cnn'} key={item.id} className="grid gap-3 border-b border-[#edf1eb] px-5 py-4 transition hover:bg-[#fbfcf9] md:grid-cols-[1.8fr_1fr_1fr_.7fr_.9fr] md:items-center md:gap-4 md:px-6"><div className="flex items-center gap-3"><img src={item.imageUrl} alt="" className="h-12 w-12 rounded-2xl object-cover"/><div><div className="font-bold">{item.plant}</div><div className="text-xs text-[#7e897f]">{item.disease}</div></div></div><div><span className="pill border-[#dfe8db] bg-[#f8faf6] text-[#64766a]">{item.model.toUpperCase()}</span></div><div><span className={`text-sm font-bold ${item.status==='healthy'?'text-[#54835c]':'text-[#a45b43]'}`}>{item.status==='healthy'?'Healthy':'Disease detected'}</span></div><div className="font-display font-extrabold">{(item.confidence*100).toFixed(1)}%</div><div className="flex items-center justify-between text-xs text-[#7d887f]">{item.date}<ChevronRight size={15}/></div></Link>):<div className="grid min-h-[300px] place-items-center p-8 text-center"><div><div className="mx-auto grid h-14 w-14 place-items-center rounded-2xl bg-[#e7f1e2] text-[#5b845f]"><Leaf/></div><div className="mt-4 font-display font-extrabold">No analyses yet</div><p className="mt-1 text-sm text-[#7d897f]">Run an analysis and real session results will appear here.</p></div></div>}</div></div>;
}
