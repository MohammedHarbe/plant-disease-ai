import {useState} from 'react';
import {Bot, Leaf, RotateCcw, Send, Sparkles} from 'lucide-react';
import AssistantResponse from '../components/AssistantResponse';
import {askPlantAI} from '../services/api';

interface Msg { role: 'user' | 'assistant'; text: string }

export default function Assistant() {
  const storedResult = sessionStorage.getItem('plantai:lastResult');
  let analysisContext: Record<string, unknown> | undefined;
  try {
    const parsed = storedResult ? JSON.parse(storedResult) : null;
    if (parsed?.result) analysisContext = {model: parsed.model, ...parsed.result};
  } catch {
    analysisContext = undefined;
  }

  const [messages, setMessages] = useState<Msg[]>([{role: 'assistant', text: 'Hi! I’m PlantAI, your plant health assistant. I can explain your Tomato Early Blight result, treatment options, prevention, or watering routines.'}]);
  const [text, setText] = useState('');
  const [busy, setBusy] = useState(false);

  const send = async (value = text) => {
    if (!value.trim() || busy) return;
    setMessages(current => [...current, {role: 'user', text: value.trim()}]);
    setText('');
    setBusy(true);
    try {
      const reply = await askPlantAI(value, analysisContext);
      setMessages(current => [...current, {role: 'assistant', text: reply}]);
    } catch (error) {
      const message = error instanceof Error ? error.message : 'The assistant is unavailable right now.';
      setMessages(current => [...current, {role: 'assistant', text: `Sorry, I could not reach PlantAI: ${message}`}]);
    } finally {
      setBusy(false);
    }
  };

  const suggestions = ['What is this disease?', 'How do I treat it?', 'How can I prevent it?', 'Is my plant healthy?'];

  return <div className="p-5 lg:p-9">
    <div className="mb-7"><div className="pill border-[#dbe8d6] bg-white text-[#55765c]"><Sparkles size={13} />PlantAI Assistant</div><h1 className="mt-4 font-display text-3xl font-extrabold">Your plant doctor, on demand.</h1><p className="mt-2 max-w-2xl text-sm leading-6 text-[#7b887f]">Ask plain-language questions about a diagnosis. Responses come from your configured Gemini assistant.</p></div>
    <div className="mx-auto max-w-5xl"><div className="card overflow-hidden">
      <div className="flex items-center gap-3 border-b border-[#e8eee5] bg-[#fbfcf9] p-5"><div className="grid h-11 w-11 place-items-center rounded-2xl bg-[#dcefd4] text-[#35633f]"><Bot size={21} /></div><div><div className="font-display font-extrabold">PlantAI Assistant</div><div className="flex items-center gap-1.5 text-xs text-[#738177]"><span className="h-2 w-2 rounded-full bg-[#6fae68]" />Online · context: {String(analysisContext?.plant || 'general plant care')}{analysisContext?.disease ? ` · ${String(analysisContext.disease)}` : ''}</div></div><button onClick={() => setMessages([])} className="ml-auto grid h-10 w-10 place-items-center rounded-xl text-[#879189] hover:bg-white" title="Clear chat"><RotateCcw size={16} /></button></div>
      <div className="min-h-[430px] space-y-5 bg-[#f8faf6] p-5 sm:p-7">{messages.length === 0 && <div className="grid min-h-[300px] place-items-center text-center"><div><div className="mx-auto grid h-14 w-14 place-items-center rounded-2xl bg-[#e2f1dd] text-[#4a7d51]"><Leaf /></div><div className="mt-4 font-display font-extrabold">Start a new plant conversation</div><p className="mt-1 text-sm text-[#7d897f]">Choose a prompt below or ask anything.</p></div></div>}{messages.map((message, index) => <div key={index} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}><div className={`max-w-[82%] rounded-[22px] px-4 py-3 ${message.role === 'user' ? 'rounded-br-md bg-[#173b27] text-sm leading-6 text-white' : 'rounded-bl-md border border-[#e0e9dc] bg-white shadow-sm'}`}>{message.role === 'assistant' ? <AssistantResponse text={message.text} /> : message.text}</div></div>)}{busy && <div className="flex"><div className="rounded-[22px] rounded-bl-md border border-[#e0e9dc] bg-white px-4 py-3 text-sm text-[#809087]">PlantAI is thinking<span className="animate-pulse">...</span></div></div>}</div>
      <div className="border-t border-[#e8eee5] p-5"><div className="mb-4 flex flex-wrap gap-2">{suggestions.map(suggestion => <button key={suggestion} onClick={() => void send(suggestion)} disabled={busy} className="rounded-full border border-[#dce7d8] bg-[#f8faf6] px-3.5 py-2 text-xs font-semibold text-[#55705b] transition hover:-translate-y-0.5 hover:bg-[#eef6ea] disabled:opacity-50">{suggestion}</button>)}</div><form onSubmit={event => {event.preventDefault(); void send();}} className="flex gap-2 rounded-2xl border border-[#dce6d9] bg-[#fbfcfa] p-2 focus-within:border-[#98bd90]"><input value={text} onChange={event => setText(event.target.value)} placeholder="Ask about your plant..." className="min-w-0 flex-1 bg-transparent px-3 text-sm outline-none placeholder:text-[#a0aaa2]" /><button className="grid h-11 w-11 shrink-0 place-items-center rounded-xl bg-[#173b27] text-white transition hover:bg-[#2a5a3a] disabled:opacity-40" disabled={!text.trim() || busy} title="Send message"><Send size={17} /></button></form></div>
    </div></div>
  </div>;
}