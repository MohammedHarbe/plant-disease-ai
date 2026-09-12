import type {HistoryItem,CnnResult} from '../types';
export const demoPlantImage='https://images.unsplash.com/photo-1591857177580-dc82b9ac4e1e?auto=format&fit=crop&w=1200&q=85';
export const cnnDemo:CnnResult={plant:'Tomato',disease:'Early Blight',confidence:.924,inferenceMs:132,imageUrl:demoPlantImage,predictions:[{label:'Early Blight',confidence:.924},{label:'Late Blight',confidence:.048},{label:'Healthy',confidence:.028}]};
export const historySeed:HistoryItem[]=[
{id:'a2',plant:'Pepper',disease:'Healthy',model:'cnn',confidence:.981,date:'Yesterday, 4:18 PM',status:'healthy',imageUrl:'https://images.unsplash.com/photo-1563565375-f3fdfdbefa83?auto=format&fit=crop&w=500&q=80'},
{id:'a3',plant:'Potato',disease:'Late Blight',model:'cnn',confidence:.886,date:'Sep 06, 9:12 AM',status:'diseased',imageUrl:'https://images.unsplash.com/photo-1518977676601-b53f82aba655?auto=format&fit=crop&w=500&q=80'}];
