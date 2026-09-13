import {useEffect,useMemo,useState} from 'react';
import {BarChart3,GitCompare,Info,Sparkles} from 'lucide-react';
import {Link} from 'react-router-dom';
import Confidence from '../components/Confidence';
import {predictCnn,predictYolo} from '../services/api';
import {readStoredAnalysis,saveAnalysisResult} from '../services/analysisStore';
import type {StoredAnalysisResults} from '../types';
import {ResponsiveContainer,BarChart,Bar,XAxis,YAxis,Tooltip,CartesianGrid} from 'recharts';

export default function Compare(){
  const [analysis,setAnalysis]=useState<StoredAnalysisResults>(()=>readStoredAnalysis());
  const [loading,setLoading]=useState(false);
  const [error,setError]=useState('');
  const imageUrl=analysis.imageUrl||analysis.yolo?.imageUrl||analysis.cnn?.imageUrl;

  useEffect(()=>{
    if(!imageUrl||(analysis.yolo&&analysis.cnn))return;
    const sourceImage=imageUrl;

    let ignore=false;
    async function loadMissingResults(){
      setLoading(true);
      setError('');
      try{
        if(!analysis.yolo){
          const yoloResult=await predictYolo(sourceImage);
          saveAnalysisResult('yolo',yoloResult,sourceImage);
        }
        if(!analysis.cnn){
          const cnnResult=await predictCnn(sourceImage);
          saveAnalysisResult('cnn',cnnResult,sourceImage);
        }
        if(!ignore)setAnalysis(readStoredAnalysis());
      }catch{
        if(!ignore)setError('Could not run both models for comparison. Please try again.');
      }finally{
        if(!ignore)setLoading(false);
      }
    }

    void loadMissingResults();
    return ()=>{ignore=true;};
  },[imageUrl,analysis.yolo,analysis.cnn]);

  const yolo=analysis.yolo;
  const cnn=analysis.cnn;
  const metrics=useMemo(()=>yolo&&cnn?[
    {name:'Confidence',YOLO:yolo.confidence*100,CNN:cnn.confidence*100},
    {name:'Inference (ms)',YOLO:yolo.inferenceMs,CNN:cnn.inferenceMs},
  ]:[],[yolo,cnn]);

  if(!imageUrl)return <EmptyState title="Run an analysis first" text="Upload an image so PlantAI can compare real YOLO and CNN results."/>;
  if(loading&&(!yolo||!cnn))return <EmptyState title="Running comparison" text="PlantAI is running the missing model on your original uploaded image."/>;
  if(error&&(!yolo||!cnn))return <EmptyState title="Comparison unavailable" text={error}/>;
  if(!yolo||!cnn)return <EmptyState title="Run both models first" text="The comparison page only displays real YOLO and CNN outputs."/>;

  const confidence=(yolo.confidence*100).toFixed(1);
  const cnnConfidence=(cnn.confidence*100).toFixed(1);

  return <div className="p-5 lg:p-9">
    <div className="mb-7">
      <div className="pill border-[#dbe8d6] bg-white text-[#58775d]"><GitCompare size={13}/>Latest connected scan</div>
      <h1 className="mt-4 font-display text-3xl font-extrabold">YOLO vs CNN</h1>
      <p className="mt-2 max-w-2xl text-sm leading-6 text-[#7b887f]">Compare real outputs from both connected models for the same original uploaded image.</p>
    </div>
    <div className="card overflow-hidden p-4">
      <div className="relative flex h-[270px] items-center justify-center overflow-hidden rounded-[25px] bg-[#f5f7f2]">
        <img src={imageUrl} alt="Latest plant scan" className="block h-auto max-h-full w-auto max-w-full object-contain object-center"/>
        <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-[#102719]/70 to-transparent p-5 text-white">
          <div className="text-xs font-bold uppercase tracking-widest text-white/60">Same input image</div>
          <div className="mt-1 font-display text-xl font-extrabold">{yolo.plant} scan</div>
        </div>
      </div>
    </div>
    <div className="mt-6 grid gap-5 lg:grid-cols-2">
      <ModelCard name="YOLO" subtitle="Detection + Classification" confidence={yolo.confidence} disease={yolo.disease} details={`Detected ${yolo.objectsDetected} localized regions`} color="bg-[#173b27]"/>
      <ModelCard name="Pre-trained CNN" subtitle="Image Classification" confidence={cnn.confidence} disease={cnn.disease} details="Top prediction for the full image" color="bg-[#486b4f]"/>
    </div>
    <div className="mt-6 grid gap-6 xl:grid-cols-[1fr_430px]">
      <div className="card overflow-hidden">
        <div className="border-b border-[#edf1eb] p-6">
          <h2 className="font-display text-xl font-extrabold">Comparison table</h2>
          <p className="mt-1 text-xs text-[#869188]">Both values come from live backend predictions for the same upload.</p>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-[#f8faf6] text-xs uppercase tracking-wider text-[#7d897f]"><tr><th className="px-6 py-4">Metric</th><th className="px-6 py-4">YOLO</th><th className="px-6 py-4">CNN</th></tr></thead>
            <tbody className="divide-y divide-[#edf1eb]">
              <Row a="Task" b="Detection + Classification" c="Classification"/>
              <Row a="Confidence" b={`${confidence}%`} c={`${cnnConfidence}%`}/>
              <Row a="Inference Time" b={`${yolo.inferenceMs} ms`} c={`${cnn.inferenceMs} ms`}/>
              <Row a="Model Type" b="YOLO vision detector" c="Pre-trained CNN"/>
              <Row a="Accuracy" b="Requires evaluation data" c="Requires evaluation data"/>
              <Row a="Precision" b="Requires evaluation data" c="Requires evaluation data"/>
              <Row a="Recall" b="Requires evaluation data" c="Requires evaluation data"/>
              <Row a="F1 / mAP" b="Requires evaluation data" c="Requires evaluation data"/>
            </tbody>
          </table>
        </div>
      </div>
      <div className="card p-6">
        <div className="flex items-start justify-between">
          <div><h2 className="font-display text-lg font-extrabold">Visual benchmark</h2><p className="mt-1 text-xs text-[#849087]">Confidence and latency from real predictions.</p></div>
          <BarChart3 className="text-[#668b6b]" size={20}/>
        </div>
        <div className="mt-6 h-[280px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={metrics} margin={{top:10,right:8,left:-20,bottom:0}}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e6ece3"/>
              <XAxis dataKey="name" tick={{fontSize:11}} axisLine={false} tickLine={false}/>
              <YAxis tick={{fontSize:10}} axisLine={false} tickLine={false}/>
              <Tooltip contentStyle={{borderRadius:16,border:'1px solid #e2e9df',boxShadow:'0 12px 30px rgba(20,50,30,.08)'}}/>
              <Bar dataKey="YOLO" fill="#173b27" radius={[8,8,0,0]}/>
              <Bar dataKey="CNN" fill="#87a87d" radius={[8,8,0,0]}/>
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="rounded-2xl bg-[#f7faf5] p-4 text-xs leading-5 text-[#748177]"><Info size={14} className="mr-2 inline text-[#668a6a]"/>Accuracy, precision, recall, F1 and mAP require a labeled evaluation dataset.</div>
      </div>
    </div>
    <div className="mt-6 rounded-[28px] border border-[#dce9d7] bg-[#eef6e9] p-5">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div><div className="flex items-center gap-2 font-bold text-[#31563a]"><Sparkles size={16}/>Want to test another image?</div><p className="mt-1 text-xs text-[#718175]">Run both models on a fresh scan, then compare their outputs here.</p></div>
        <Link to="/analyze" className="btn-primary">New analysis</Link>
      </div>
    </div>
  </div>;
}

function EmptyState({title,text}:{title:string;text:string}){
  return <div className="grid min-h-[420px] place-items-center p-8 text-center"><div><div className="font-display text-2xl font-extrabold">{title}</div><p className="mt-2 text-sm text-[#7b887e]">{text}</p><Link to="/analyze" className="btn-primary mt-5 inline-flex">Start analysis</Link></div></div>;
}

function ModelCard({name,subtitle,confidence,disease,details,color}:{name:string;subtitle:string;confidence:number;disease:string;details:string;color:string}){
  return <div className="card overflow-hidden">
    <div className={`${color} p-6 text-white`}>
      <div className="flex items-center justify-between">
        <div><div className="text-xs font-bold uppercase tracking-[.18em] text-white/55">Model</div><div className="mt-1 font-display text-2xl font-extrabold">{name}</div><div className="mt-1 text-sm text-white/65">{subtitle}</div></div>
        <div className="grid h-11 w-11 place-items-center rounded-2xl bg-white/10"><GitCompare size={19}/></div>
      </div>
    </div>
    <div className="p-6"><div className="grid gap-5 sm:grid-cols-2"><div><div className="text-[11px] font-bold uppercase tracking-wider text-[#8a948c]">Diagnosis</div><div className="mt-1 font-display text-lg font-extrabold">{disease}</div><div className="mt-1 text-xs text-[#7d897f]">{details}</div></div><Confidence value={confidence}/></div></div>
  </div>;
}

function Row({a,b,c}:{a:string;b:string;c:string}){
  return <tr><td className="px-6 py-4 font-bold text-[#3e5143]">{a}</td><td className="px-6 py-4 text-[#68766c]">{b}</td><td className="px-6 py-4 text-[#68766c]">{c}</td></tr>;
}
