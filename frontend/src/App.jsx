import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  LayoutDashboard, 
  MessageSquare, 
  ShieldAlert, 
  TrendingUp, 
  ArrowRight, 
  RefreshCcw,
  AlertTriangle,
  CheckCircle2,
  ChevronRight,
  User,
  Bot,
  Zap,
  Activity,
  CreditCard,
  History,
  Target,
  Play
} from 'lucide-react';

const API_BASE = 'http://localhost:8001';

function App() {
  const [state, setState] = useState(null);
  const [level, setLevel] = useState('Easy');
  const [loading, setLoading] = useState(true);
  const [actionInProgress, setActionInProgress] = useState(false);
  const [isAutoRunning, setIsAutoRunning] = useState(false);

  const fetchState = async () => {
    try {
      const res = await axios.get(`${API_BASE}/state`);
      setState(res.data);
      setLoading(false);
    } catch (err) {
      console.error("Failed to fetch state", err);
    }
  };

  const handleReset = async (newLevel = level) => {
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/reset?level=${newLevel}`);
      setLevel(newLevel);
      await fetchState();
    } catch (err) {
      console.error("Reset failed", err);
    }
  };

  const handleStep = async (actionType) => {
    setActionInProgress(true);
    try {
      const action = {
        action_type: actionType,
        explanation: `User manually selected ${actionType} for this case.`,
        response_text: `Thank you for contacting us. We have processed a ${actionType.toLowerCase()} for your order.`
      };
      await axios.post(`${API_BASE}/step`, action);
      await fetchState();
    } catch (err) {
      console.error("Step failed", err);
    }
    setActionInProgress(false);
  };

  const runAiAgent = async () => {
    setIsAutoRunning(true);
    try {
      // Simulate real agent loop: Easy -> Medium -> Hard
      const targetLevels = ['Easy', 'Medium', 'Hard'];
      
      for (const targetLevel of targetLevels) {
        // 1. Reset to the specific level
        setLoading(true);
        const resetResp = await axios.post(`${API_BASE}/reset?level=${targetLevel}`);
        const observation = resetResp.data;
        setLevel(targetLevel);
        await fetchState();
        
        // 2. Simulate "Agent Thinking"
        await new Promise(r => setTimeout(r, 2000));
        
        // 3. Decide action based on simplistic agent logic (demo purposes)
        let actionType = 'RESPOND';
        if (observation.order_value > 1000) actionType = 'ESCALATE';
        else if (observation.product_issue === 'DAMAGED' || observation.product_issue === 'WRONG_ITEM') {
            actionType = targetLevel === 'Hard' ? 'ESCALATE' : 'REFUND';
        }

        // 4. Perform Task Step
        const action = {
          action_type: actionType,
          explanation: `Automated AI Agent selected ${actionType} based on order value ($${observation.order_value}) and issue type (${observation.product_issue}).`,
          response_text: `System Agent: I have determined that ${actionType} is the optimal resolution for your concern.`
        };
        
        await axios.post(`${API_BASE}/step`, action);
        await fetchState();
        
        // 5. Wait to let user see step result
        await new Promise(r => setTimeout(r, 3000));
      }
    } catch (err) {
      console.error("AI Agent Run failed", err);
    }
    setIsAutoRunning(false);
  };

  useEffect(() => {
    handleReset('Easy');
  }, []);

  if (loading || !state) return (
    <div className="h-screen w-screen flex flex-col items-center justify-center bg-slate-950">
      <motion.div 
        animate={{ rotate: 360 }} 
        transition={{ repeat: Infinity, duration: 2, ease: "linear" }}
        className="mb-4"
      >
        <Zap className="text-yellow-500 w-12 h-12" fill="currentColor" />
      </motion.div>
      <p className="text-slate-500 font-medium tracking-widest text-xs uppercase">Initializing AgentDesk AI...</p>
    </div>
  );

  const { observation, cumulative_reward, done, info, step_count, reward: stepReward } = state;

  return (
    <div className="flex h-screen bg-slate-950 text-slate-200 selection:bg-indigo-500/30">
      {/* Sidebar Navigation */}
      <aside className="w-72 border-r border-white/[0.05] bg-slate-900/40 backdrop-blur-3xl flex flex-col">
        <div className="p-8 mb-4">
          <div className="flex items-center gap-3">
             <div className="w-10 h-10 bg-gradient-to-br from-yellow-400 to-amber-600 rounded-full flex items-center justify-center shadow-lg shadow-yellow-500/20">
                <LayoutDashboard className="text-white w-6 h-6" />
             </div>
             <span className="font-display font-bold text-2xl tracking-tight text-white">AgentDesk AI</span>
          </div>
        </div>

        <div className="px-4 flex-1 space-y-1">
          <p className="px-4 text-[11px] font-bold text-slate-500 uppercase tracking-widest mb-4">Core Simulations</p>
          {[
            { id: 'Easy', icon: MessageSquare, desc: 'Support & Inquiries' },
            { id: 'Medium', icon: Activity, desc: 'Product Issues' },
            { id: 'Hard', icon: ShieldAlert, desc: 'Policy & Fraud' }
          ].map((item) => (
            <button
              key={item.id}
              disabled={isAutoRunning}
              onClick={() => handleReset(item.id)}
              className={`w-full group flex items-center gap-4 px-4 py-4 rounded-2xl transition-all duration-300 ${
                level === item.id 
                ? 'bg-indigo-500/10 border border-indigo-500/20 text-white shadow-xl shadow-black/20' 
                : 'text-slate-400 hover:bg-white/[0.03] border border-transparent'
              } ${isAutoRunning ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              <item.icon className={`w-5 h-5 ${level === item.id ? 'text-indigo-400' : 'text-slate-500 group-hover:text-slate-300'}`} />
              <div className="flex flex-col text-left">
                 <span className="text-sm font-semibold">{item.id} Task</span>
                 <span className="text-[10px] opacity-50">{item.desc}</span>
              </div>
              {level === item.id && <motion.div layoutId="active" className="ml-auto w-1.5 h-1.5 bg-indigo-500 rounded-full" />}
            </button>
          ))}
        </div>

        <div className="p-6 space-y-4">
            <button 
                onClick={runAiAgent}
                disabled={isAutoRunning || done}
                className={`w-full py-4 rounded-2xl font-bold flex items-center justify-center gap-2 transition-all shadow-lg ${
                    isAutoRunning 
                    ? 'bg-indigo-500/20 text-indigo-400 cursor-not-allowed' 
                    : 'bg-indigo-600 text-white hover:bg-indigo-500 shadow-indigo-500/20 active:scale-[0.98]'
                }`}
            >
                {isAutoRunning ? <RefreshCcw className="animate-spin w-4 h-4" /> : <Play className="w-4 h-4" filled />}
                {isAutoRunning ? 'AGENT RUNNING...' : 'RUN AI AGENT'}
            </button>

           <div className="glass-card rounded-3xl p-6 relative overflow-hidden group">
              <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-500/10 rounded-full -mr-16 -mt-16 blur-3xl group-hover:scale-150 transition-transform duration-700" />
              <div className="relative z-10">
                 <div className="flex items-center gap-2 mb-2">
                    <TrendingUp size={14} className="text-cyan-400" />
                    <span className="text-[10px] font-bold text-slate-500 uppercase">Total Reward</span>
                 </div>
                 <div className="flex items-baseline gap-1 mb-3">
                    <span className="text-3xl font-display font-bold text-white leading-none">{cumulative_reward.toFixed(1)}</span>
                 </div>
                 <div className="h-1.5 bg-white/5 rounded-full overflow-hidden">
                    <motion.div 
                      className="h-full bg-gradient-to-r from-indigo-500 to-cyan-400" 
                      initial={{ width: 0 }} 
                      animate={{ width: `${Math.min(100, Math.max(0, (cumulative_reward + 10) * 5))}%` }}
                    />
                 </div>
              </div>
           </div>
        </div>
      </aside>

      {/* Main Console */}
      <main className="flex-1 flex flex-col relative overflow-hidden">
        {/* Top Navbar */}
        <header className="h-20 border-b border-white/[0.05] px-8 flex items-center justify-between bg-slate-900/20 backdrop-blur-md sticky top-0 z-50">
           <div className="flex items-center gap-4">
              <div className={`w-3 h-3 rounded-full ${done ? 'bg-rose-500 shadow-lg shadow-rose-500/40' : 'bg-emerald-500 shadow-lg shadow-emerald-500/40 animate-pulse'}`} />
              <div>
                <h2 className="text-sm font-bold text-white tracking-wide uppercase">AI Execution Environment</h2>
                <div className="flex items-center gap-2 text-[10px] text-slate-500 font-mono">
                   <span>ID: {observation.task_id}</span>
                   <span>•</span>
                   <span>STEP: {step_count}</span>
                </div>
              </div>
           </div>
           
           <div className="flex items-center gap-6">
              <div className="flex items-center gap-8 px-6 py-2 glass rounded-2xl">
                 <div className="flex flex-col items-center">
                    <span className="text-[10px] text-slate-500 uppercase font-bold">Latency</span>
                    <span className="text-xs font-mono text-emerald-400">142ms</span>
                 </div>
                 <div className="w-px h-6 bg-white/10" />
                 <div className="flex flex-col items-center">
                    <span className="text-[10px] text-slate-500 uppercase font-bold">Accuracy</span>
                    <span className="text-xs font-mono text-indigo-400">98.2%</span>
                 </div>
              </div>
              <button 
                onClick={() => handleReset()} 
                disabled={isAutoRunning}
                className={`p-3 bg-white/[0.03] hover:bg-white/[0.08] border border-white/[0.05] rounded-xl text-slate-400 transition-all active:scale-95 ${isAutoRunning ? 'opacity-30' : ''}`}
              >
                <RefreshCcw size={18} />
              </button>
           </div>
        </header>

        <div className="flex-1 grid grid-cols-12 overflow-hidden bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-indigo-900/10 via-transparent to-transparent">
          {/* Simulation Viewport */}
          <section className="col-span-8 p-8 overflow-y-auto space-y-8 flex flex-col h-full">
             
             {/* Case Header Card */}
             <motion.div 
               initial={{ opacity: 0, y: 30 }}
               animate={{ opacity: 1, y: 0 }}
               className="glass rounded-3xl p-8 relative overflow-hidden"
             >
                <div className="absolute -top-24 -right-24 w-64 h-64 bg-indigo-500/10 rounded-full blur-[100px]" />
                <div className="relative z-10">
                   <div className="flex items-center justify-between mb-8">
                      <div className="flex items-center gap-4">
                         <div className="w-14 h-14 bg-gradient-to-br from-indigo-500/20 to-cyan-500/20 rounded-2xl flex items-center justify-center border border-indigo-500/20">
                            <User className="text-indigo-400 w-7 h-7" />
                         </div>
                         <div>
                            <h3 className="text-xl font-bold text-white tracking-tight">Active Customer Inquiry</h3>
                            <div className="flex gap-2 mt-1">
                               <span className="px-2 py-0.5 rounded-md bg-indigo-500/10 text-[9px] font-bold text-indigo-400 border border-indigo-500/10 uppercase tracking-tighter">New Case</span>
                               <span className={`px-2 py-0.5 rounded-md text-[9px] font-bold border uppercase tracking-tighter ${
                                 observation.order_value > 1000 ? 'bg-rose-500/10 text-rose-400 border-rose-500/10' : 'bg-slate-500/10 text-slate-400 border-slate-500/10'
                               }`}>
                                 {observation.order_value > 1000 ? 'High Priority' : 'Standard Priority'}
                               </span>
                            </div>
                         </div>
                      </div>
                   </div>

                   <p className="text-2xl font-display font-medium leading-normal text-slate-100 max-w-3xl mb-10">
                     "{observation.customer_query}"
                   </p>

                   <div className="grid grid-cols-4 gap-6">
                      <ProfileMetric icon={CreditCard} label="Order Value" value={`$${observation.order_value}`} />
                      <ProfileMetric icon={Bot} label="Issue Category" value={observation.product_issue.replace('_', ' ')} />
                      <ProfileMetric icon={Target} label="Customer Tier" value={observation.customer_type} />
                      <SentimentMetric value={0.7} />
                   </div>
                </div>
             </motion.div>

             {/* Action Grid */}
             <div className="space-y-4">
                <div className="flex items-center justify-between px-2">
                   <div className="flex items-center gap-2">
                        <Zap size={14} className="text-yellow-400" />
                        <span className="text-xs font-bold text-slate-500 uppercase tracking-widest">Execution Engine</span>
                   </div>
                   {actionInProgress && (
                       <div className="flex items-center gap-2 text-indigo-400 text-[10px] font-bold animate-pulse uppercase">
                           <RefreshCcw size={10} className="animate-spin" />
                           Processing Next token...
                       </div>
                   )}
                </div>
                <div className="grid grid-cols-2 gap-4">
                   {[
                     { id: 'REFUND', desc: 'Process immediate monetary reimbursement', color: 'rose' },
                     { id: 'REPLACE', desc: 'Issue replacement fulfillment for item', color: 'cyan' },
                     { id: 'ESCALATE', desc: 'Transfer to senior human administrator', color: 'indigo' },
                     { id: 'RESPOND', desc: 'Provide informational status response', color: 'emerald' }
                   ].map((btn) => (
                      <button
                        key={btn.id}
                        disabled={done || actionInProgress || isAutoRunning}
                        onClick={() => handleStep(btn.id)}
                        className={`group p-6 rounded-[2rem] border border-white/[0.05] flex items-center gap-6 transition-all duration-300 relative overflow-hidden ${
                          (done || actionInProgress || isAutoRunning) ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:border-indigo-500/50 hover:bg-slate-900 shadow-xl hover:shadow-indigo-500/5 hover:-translate-y-1'
                        }`}
                      >
                         <div className={`w-12 h-12 rounded-2xl bg-slate-800/50 flex items-center justify-center group-hover:scale-110 transition-transform duration-500`}>
                            <ArrowRight size={20} className="text-slate-500 group-hover:text-indigo-400" />
                         </div>
                         <div className="text-left flex-1">
                            <p className="font-bold text-lg text-white group-hover:text-indigo-400 transition-colors tracking-tight">{btn.id}</p>
                            <p className="text-xs text-slate-500 mt-0.5 line-clamp-1">{btn.desc}</p>
                         </div>
                         <div className={`absolute bottom-0 left-0 w-full h-1 transition-all duration-500 origin-left scale-x-0 group-hover:scale-x-100 bg-indigo-500`} />
                      </button>
                   ))}
                </div>
             </div>
          </section>

          {/* Feedback & Analytics Panel */}
          <aside className="col-span-4 border-l border-white/[0.05] p-8 space-y-8 flex flex-col h-full bg-slate-900/50">
             <div>
                <h4 className="text-xs font-bold text-slate-500 mb-6 uppercase tracking-[0.2em]">Step Feedback</h4>
                {done ? (
                  <motion.div 
                    initial={{ opacity: 0, x: 20 }} 
                    animate={{ opacity: 1, x: 0 }}
                    className={`p-8 rounded-[2.5rem] flex flex-col items-center text-center relative overflow-hidden group ${
                      stepReward > 0 ? 'bg-emerald-500/10 border border-emerald-500/20' : 'bg-rose-500/10 border border-rose-500/20'
                    }`}
                  >
                     <div className={`absolute -bottom-12 -right-12 w-48 h-48 rounded-full blur-[80px] ${stepReward > 0 ? 'bg-emerald-500/20' : 'bg-rose-500/20'}`} />
                     
                     <div className={`w-20 h-20 rounded-3xl flex items-center justify-center mb-6 shadow-2xl ${
                        stepReward > 0 ? 'bg-emerald-500 text-white' : 'bg-rose-500 text-white'
                     }`}>
                        {stepReward > 0 ? <CheckCircle2 size={40} /> : <AlertTriangle size={40} />}
                     </div>
                     <h5 className="font-display font-bold text-3xl text-white mb-2">{stepReward > 0 ? 'Optimal' : 'Suboptimal'}</h5>
                     <p className="text-sm text-slate-400 font-medium leading-relaxed px-4">
                        {info.reason}
                     </p>
                     
                     <div className="w-full h-px bg-white/10 my-8" />
                     
                     <div className="grid grid-cols-1 gap-4 w-full">
                        <div className="bg-black/20 p-4 rounded-3xl border border-white/5">
                           <p className="text-[10px] text-slate-500 font-bold uppercase mb-1">Step Reward</p>
                           <p className={`text-2xl font-display font-bold ${stepReward > 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                               {stepReward > 0 ? `+${stepReward}` : stepReward}
                            </p>
                        </div>
                     </div>

                     <button 
                       onClick={() => handleReset()}
                       disabled={isAutoRunning}
                       className={`mt-8 w-full py-4 rounded-2xl bg-white text-slate-900 font-bold hover:bg-slate-200 transition-all flex items-center justify-center gap-2 text-sm ${isAutoRunning ? 'opacity-30' : ''}`}
                     >
                       <RefreshCcw size={16} /> NEXT SCENARIO
                     </button>
                  </motion.div>
                ) : (
                  <div className="p-12 border-2 border-dashed border-white/5 rounded-[2.5rem] flex flex-col items-center justify-center text-center opacity-60">
                     <motion.div 
                        animate={actionInProgress ? { rotate: 360 } : {}} 
                        transition={{ repeat: Infinity, duration: 2, ease: "linear" }}
                        className="mb-4"
                     >
                        <Bot size={40} className={actionInProgress ? 'text-indigo-400' : 'text-slate-700'} />
                     </motion.div>
                     <p className="text-sm font-medium text-slate-500">
                         {actionInProgress ? 'Agent is executing action...' : 'Awaiting Agent step payload...'}
                     </p>
                     <p className="text-[10px] text-slate-600 mt-2 font-mono uppercase">
                         {actionInProgress ? 'Processing Transaction' : 'Listen channel active'}
                     </p>
                  </div>
                )}
             </div>

             <div className="flex-1 flex flex-col justify-end">
                <div className="p-6 glass-card rounded-[2rem] border-white/5">
                   <div className="flex items-center gap-2 mb-4">
                      <div className="w-2 h-2 rounded-full bg-indigo-500 shadow-md shadow-indigo-500/50" />
                      <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest leading-none mt-0.5">Live Environment Stream</span>
                   </div>
                   <div className="max-h-64 overflow-y-auto pr-2 custom-scroll">
                      <pre className="text-[10px] font-mono leading-relaxed text-indigo-300/80">
                         {JSON.stringify(observation, null, 2)}
                      </pre>
                   </div>
                </div>
             </div>
          </aside>
        </div>
      </main>
    </div>
  );
}

function ProfileMetric({ icon: Icon, label, value }) {
  return (
    <div className="flex flex-col gap-2 p-5 rounded-3xl bg-slate-900 border border-white/5 group hover:border-indigo-500/30 transition-all duration-300 hover:shadow-2xl hover:shadow-black/50">
      <div className="flex items-center gap-2 text-slate-500">
         <Icon size={14} className="group-hover:text-indigo-400 transition-colors" />
         <span className="text-[11px] font-bold uppercase tracking-wider">{label}</span>
      </div>
      <p className="text-lg font-bold text-white group-hover:text-indigo-400 transition-colors tracking-tight">{value}</p>
    </div>
  );
}

function SentimentMetric({ value }) {
  return (
    <div className="flex flex-col gap-2 p-5 rounded-3xl bg-slate-900 border border-white/5 group hover:border-indigo-500/30 transition-all duration-300 hover:shadow-2xl hover:shadow-black/50">
      <div className="flex items-center gap-2 text-slate-500">
         <TrendingUp size={14} className="group-hover:text-cyan-400 transition-colors" />
         <span className="text-[11px] font-bold uppercase tracking-wider">Sentiment</span>
      </div>
      <div className="flex items-center gap-3">
         <div className="flex-1 h-2 bg-slate-800 rounded-full overflow-hidden">
            <motion.div 
              initial={{ width: 0 }}
              animate={{ width: `${value * 100}%` }}
              className={`h-full ${value < 0.3 ? 'bg-rose-500' : value < 0.7 ? 'bg-amber-400' : 'bg-emerald-500'}`}
            />
         </div>
         <span className={`text-sm font-bold ${value < 0.3 ? 'text-rose-400' : 'text-emerald-400'}`}>
            {(value * 100).toFixed(0)}%
         </span>
      </div>
    </div>
  );
}

export default App;
