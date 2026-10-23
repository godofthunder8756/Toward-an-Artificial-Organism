import fs from "node:fs/promises";
import path from "node:path";
import crypto from "node:crypto";
import sharp from "sharp";

const ROOT = path.dirname(new URL(import.meta.url).pathname).replace(/^\/(.:\/)/, "$1");
const OUT = path.join(ROOT, "paperc_figures_v1");
const RAW = path.join(ROOT, "INSTRUMENT0_STAGE5_RAW_V1.jsonl");

const COLORS = {
  ink: "#102A43", muted: "#52667A", grid: "#D9E2EC", teal: "#007C83",
  orange: "#E36B2C", purple: "#6B5AA6", green: "#2F855A", red: "#C53030",
  blue: "#2B6CB0", light: "#F5F8FA", white: "#FFFFFF"
};

const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&apos;"}[c]));
const median = (a) => { const b=[...a].sort((x,y)=>x-y), n=b.length; return n%2?b[(n-1)/2]:(b[n/2-1]+b[n/2])/2; };
const sha = (b) => crypto.createHash("sha256").update(b).digest("hex");
const svgStart = (w,h,title,desc) => `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" role="img" aria-labelledby="title desc"><title id="title">${esc(title)}</title><desc id="desc">${esc(desc)}</desc><rect width="100%" height="100%" fill="${COLORS.white}"/><style>text{font-family:Arial,'Noto Sans',sans-serif;fill:${COLORS.ink}}.title{font-size:42px;font-weight:700}.sub{font-size:24px;fill:${COLORS.muted}}.label{font-size:25px;font-weight:700}.body{font-size:22px}.small{font-size:19px;fill:${COLORS.muted}}.axis{font-size:18px;fill:${COLORS.muted}}.direct{font-size:20px;font-weight:700}</style>`;
const line = (x1,y1,x2,y2,stroke=COLORS.grid,width=2,dash="") => `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${stroke}" stroke-width="${width}"${dash?` stroke-dasharray="${dash}"`:""}/>`;
const text = (x,y,s,cls="body",anchor="start") => `<text x="${x}" y="${y}" class="${cls}" text-anchor="${anchor}">${esc(s)}</text>`;

function endpointValue(row, ep) {
  if (ep === "E1") return row.TRUE.loss_sum / row.TRUE.n_tokens;
  if (ep === "E2") return row.SWAP.mean_nll - row.TRUE.mean_nll;
  if (ep === "E3") return row.TRUE.stop_mass;
  const a1 = row.E4_order1.logp_A > row.E4_order1.logp_B ? 1 : 0;
  const b2 = row.E4_order2.logp_B > row.E4_order2.logp_A ? 1 : 0;
  return (a1 + b2) / 2;
}

function buildDoseData(rows) {
  const doses=[...new Set(rows.map(r=>r.dose))].sort((a,b)=>a-b);
  const slugs=[...new Set(rows.map(r=>r.slug))].sort();
  const out={doses,slugs,endpoints:{}};
  for (const ep of ["E1","E2","E3","E4"]) {
    out.endpoints[ep]=doses.map(dose=>{
      const values=slugs.map(slug=>{
        const v=rows.filter(r=>r.dose===dose&&r.slug===slug).map(r=>endpointValue(r,ep));
        return ep==="E4"?v.reduce((a,b)=>a+b,0)/v.length:median(v);
      });
      return {dose,values,median:median(values)};
    });
  }
  return out;
}

function figure1() {
  const w=1800,h=920, y=360, boxW=292, boxH=210, gap=40, start=95;
  const stages=[
    ["1","Known-answer fixtures","39 / 39 PASS","Synthetic data only"],
    ["2","Proxy compatibility","30 / 30 PASS","No primary outcomes"],
    ["3","Instrument freeze","43 artifacts","Rules and bytes fixed"],
    ["4","Prediction seal","Fable + Opus","Primary raw absent"],
    ["5","One-shot run","261 rows","9 points × 29 items"]
  ];
  let s=svgStart(w,h,"Figure 1. INSTRUMENT-0 study sequence","Five-stage sequence from known-answer fixtures to the one-shot primary run.");
  s+=text(90,90,"INSTRUMENT-0: measurement before interpretation","title");
  s+=text(90,135,"Every gate was completed before the primary 261-row matrix was interpreted.","sub");
  stages.forEach((st,i)=>{
    const x=start+i*(boxW+gap);
    if(i<stages.length-1){s+=line(x+boxW,y+boxH/2,x+boxW+gap-15,y+boxH/2,COLORS.muted,5);s+=`<path d="M ${x+boxW+gap-25} ${y+boxH/2-12} L ${x+boxW+gap-5} ${y+boxH/2} L ${x+boxW+gap-25} ${y+boxH/2+12}" fill="none" stroke="${COLORS.muted}" stroke-width="5"/>`;}
    s+=`<rect x="${x}" y="${y}" width="${boxW}" height="${boxH}" rx="12" fill="${i===4?'#E8F5F3':COLORS.light}" stroke="${i===4?COLORS.teal:COLORS.grid}" stroke-width="3"/>`;
    s+=`<circle cx="${x+42}" cy="${y+42}" r="25" fill="${i===4?COLORS.teal:COLORS.ink}"/><text x="${x+42}" y="${y+51}" font-family="Arial, Helvetica, sans-serif" font-size="24" text-anchor="middle" style="fill:#FFFFFF">${st[0]}</text>`;
    s+=text(x+25,y+92,st[1],"label");s+=text(x+25,y+132,st[2],"body");s+=text(x+25,y+170,st[3],"small");
  });
  s+=`<rect x="95" y="680" width="1610" height="115" rx="10" fill="#FFF7ED" stroke="${COLORS.orange}" stroke-width="3"/>`;
  s+=text(125,725,"Preservation rule","label");
  s+=text(390,725,"If a defect appeared, stop and preserve it; do not repair the rule and reuse the same raw data.","body");
  s+=text(125,765,"Primary inference unit: 16 equal-weight slugs. The 29 items are within-slug repetitions.","small");
  return s+"</svg>";
}

function panel(data, x,y,w,h, ep, titleStr, unit, color, refs=[]) {
  const all=data.flatMap(d=>d.values), min0=Math.min(...all,...refs.map(r=>r.value)), max0=Math.max(...all,...refs.map(r=>r.value));
  const pad=(max0-min0||1)*0.12, ymin=min0-pad, ymax=max0+pad;
  const px=d=>x+75+(d/192)*(w-115), py=v=>y+55+(ymax-v)/(ymax-ymin)*(h-125);
  let s=`<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${COLORS.white}" stroke="${COLORS.grid}" stroke-width="2"/>`;
  s+=text(x+25,y+36,titleStr,"label");
  for(let k=0;k<=4;k++){const v=ymin+(ymax-ymin)*k/4, yy=py(v);s+=line(x+70,yy,x+w-30,yy,COLORS.grid,1);s+=text(x+60,yy+6,v.toFixed(ep==='E4'?2:1),"axis","end");}
  for(const d of [0,48,96,144,192]){const xx=px(d);s+=line(xx,y+h-70,xx,y+h-62,COLORS.muted,2);s+=text(xx,y+h-38,String(d),"axis","middle");}
  s+=text(x+w/2,y+h-8,"Dose / evaluation point","axis","middle");
  s+=`<text x="${x+18}" y="${y+h/2}" class="axis" text-anchor="middle" transform="rotate(-90 ${x+18} ${y+h/2})">${esc(unit)}</text>`;
  refs.forEach(r=>{const yy=py(r.value);s+=line(x+70,yy,x+w-30,yy,r.color||COLORS.red,3,"12 8");if(r.value===-1){s+=text(x+82,yy+26,r.label,"small","start");}else{s+=text(x+w-35,yy-10,r.label,"small","end");}});
  data.forEach((d,di)=>{d.values.forEach((v,vi)=>{const jitter=((vi%5)-2)*2.4;s+=`<circle cx="${px(d.dose)+jitter}" cy="${py(v)}" r="4" fill="${COLORS.muted}" opacity="0.28"/>`;});});
  const pts=data.map(d=>`${px(d.dose)},${py(d.median)}`).join(" ");
  s+=`<polyline points="${pts}" fill="none" stroke="${color}" stroke-width="6"/>`;
  data.forEach(d=>{s+=`<circle cx="${px(d.dose)}" cy="${py(d.median)}" r="8" fill="${COLORS.white}" stroke="${color}" stroke-width="5"/>`;});
  s+=text(x+w-35,y+36,"dots: slugs; line: slug median","small","end");
  return s;
}

function figure2(doseData) {
  const w=1800,h=1480, pw=790,ph=570;
  let s=svgStart(w,h,"Figure 2. Dose trajectories of four endpoints","Slug-level values and equal-weight slug medians across nine evaluation points. Only d0 versus d192 is the primary contrast.");
  s+=text(90,80,"Dose trajectories reveal different failure modes","title");
  s+=text(90,125,"Small dots are 16 slug values; colored lines are equal-weight slug medians. Intermediate doses are descriptive.","sub");
  s+=panel(doseData.endpoints.E1,90,185,pw,ph,"E1","E1 — normalized NLL","nat / token",COLORS.blue);
  s+=panel(doseData.endpoints.E2,920,185,pw,ph,"E2","E2 — TRUE preference","NLL difference",COLORS.purple);
  s+=panel(doseData.endpoints.E3,90,800,pw,ph,"E3","E3 — stop-token log mass","nat",COLORS.teal,[{value:-1,label:"provisional ceiling −1.0",color:COLORS.red},{value:-20,label:"provisional floor −20.0",color:COLORS.orange}]);
  s+=panel(doseData.endpoints.E4,920,800,pw,ph,"E4","E4 — reversed-order item score","score",COLORS.orange);
  s+=text(90,1435,"Primary contrast: d0 versus d192. The curves do not establish a causal dose effect.","small");
  return s+"</svg>";
}

function figure3() {
  const w=1700,h=980, left=300, right=1550, top=225, rowH=140;
  const rows=[
    {ep:"E1",dr:7.0996,color:COLORS.blue,out:"Out-of-table STOP",note:"Decision rule did not cover the observation"},
    {ep:"E2",dr:0.6429,color:COLORS.purple,out:"NOT_SEPARABLE",note:"Observed separation below null scale"},
    {ep:"E3",dr:9.2745,color:COLORS.teal,out:"FAILED_FLOOR_CEILING",note:"Strong separation, but d192 exceeded ceiling"},
    {ep:"E4",dr:null,color:COLORS.orange,out:"UNDEFINED_ENDPOINT",note:"NULL_scale = 0 after order averaging"}
  ];
  const xmax=10, px=v=>left+(v/xmax)*(right-left);
  let s=svgStart(w,h,"Figure 3. Detection ratio did not determine endpoint usability","Detection ratios and final preregistered outcomes for four endpoints.");
  s+=text(80,75,"A large detection ratio was not enough","title");
  s+=text(80,120,"Final outcomes also depended on operating range, null construction, and decision-table coverage.","sub");
  for(const v of [0,1,3,5,7,10]){const x=px(v);s+=line(x,top-35,x,top+rowH*4-30,COLORS.grid,2,v===1||v===3?"10 8":"");s+=text(x,top-62,String(v),"axis","middle");}
  s+=text((left+right)/2,925,"Detection ratio, DR = |SEP| / NULL_scale","axis","middle");
  s+=text(px(1),top-25,"DR = 1","small","middle");s+=text(px(3),top-25,"DR = 3","small","middle");
  rows.forEach((r,i)=>{const y=top+i*rowH+45;s+=text(85,y+8,r.ep,"label");if(r.dr!==null){s+=`<circle cx="${px(r.dr)}" cy="${y}" r="15" fill="${r.color}"/>`;s+=line(left,y,px(r.dr),y,r.color,7);s+=text(px(r.dr)+22,y+7,r.dr.toFixed(2),"direct");}else{s+=text(left,y+7,"undefined","direct");}s+=text(left,y+50,r.out,"direct");s+=text(left+360,y+50,r.note,"small");});
  return s+"</svg>";
}

function figure4() {
  const w=1700,h=920, left=450, right=1510, top=235, rowH=140;
  const rows=[
    {ep:"E1",out:"OUT OF TABLE",f:0,o:0},
    {ep:"E2",out:"Row 8",f:0.10,o:0.68},
    {ep:"E3",out:"Row 3",f:0.40,o:0.39},
    {ep:"E4",out:"Row 3.5",f:0,o:0.06}
  ];
  const px=v=>left+v*(right-left);
  let s=svgStart(w,h,"Figure 4. Probability assigned to the realized outcome before the run","Sealed probabilities from Fable and Opus for the outcome that was later realized for each endpoint.");
  s+=text(80,75,"Sealed predictions preserved disagreements and misses","title");
  s+=text(80,120,"Points show probability assigned before the primary raw file existed to the outcome later realized.","sub");
  for(const v of [0,.25,.5,.75,1]){const x=px(v);s+=line(x,top-45,x,top+rowH*4-35,COLORS.grid,2);s+=text(x,top-65,v.toFixed(2),"axis","middle");}
  rows.forEach((r,i)=>{const y=top+i*rowH+35;s+=text(80,y-7,`${r.ep} — ${r.out}`,"label");s+=line(left,y-15,px(r.f),y-15,COLORS.blue,5);s+=`<circle cx="${px(r.f)}" cy="${y-15}" r="12" fill="${COLORS.blue}"/>`;s+=text(px(r.f)+18,y-8,`Fable ${r.f.toFixed(2)}`,"body");s+=line(left,y+30,px(r.o),y+30,COLORS.orange,5);s+=`<rect x="${px(r.o)-11}" y="${y+19}" width="22" height="22" fill="${COLORS.orange}"/>`;s+=text(px(r.o)+18,y+38,`Opus ${r.o.toFixed(2)}`,"body");});
  s+=text(80,855,"Four endpoints are insufficient to rank predictor quality; this is a process record, not a forecasting benchmark.","small");
  return s+"</svg>";
}

async function writeFigure(name, svg) {
  const svgPath=path.join(OUT,`${name}.svg`), pngPath=path.join(OUT,`${name}.png`);
  await fs.writeFile(svgPath,svg,"utf8");
  await sharp(Buffer.from(svg)).png({compressionLevel:9}).toFile(pngPath);
  const sb=await fs.readFile(svgPath), pb=await fs.readFile(pngPath);
  return {svg:{file:path.basename(svgPath),sha256:sha(sb),bytes:sb.length},png:{file:path.basename(pngPath),sha256:sha(pb),bytes:pb.length}};
}

export async function generate() {
  await fs.mkdir(OUT,{recursive:true});
  const rawBytes=await fs.readFile(RAW);
  const rows=rawBytes.toString("utf8").trim().split(/\r?\n/).map(JSON.parse);
  const doseData=buildDoseData(rows);
  const figures={};
  figures.figure1_instrument_sequence=await writeFigure("figure1_instrument_sequence",figure1());
  figures.figure2_endpoint_dose_trajectories=await writeFigure("figure2_endpoint_dose_trajectories",figure2(doseData));
  figures.figure3_detection_ratio_outcomes=await writeFigure("figure3_detection_ratio_outcomes",figure3());
  figures.figure4_prediction_scorecard=await writeFigure("figure4_prediction_scorecard",figure4());
  const data={schema:"mythos.paperc_figure_data.v1",source:{file:path.basename(RAW),sha256:sha(rawBytes),n_rows:rows.length},dose_data:doseData,figures};
  const db=Buffer.from(JSON.stringify(data,null,2)+"\n");
  await fs.writeFile(path.join(OUT,"PAPERC_FIGURE_DATA_V1.json"),db);
  data.figure_data_sha256=sha(db);
  const generatorBytes=await fs.readFile(new URL(import.meta.url));
  const assetNames=[
    "figure1_instrument_sequence.svg","figure1_instrument_sequence.png",
    "figure2_endpoint_dose_trajectories.svg","figure2_endpoint_dose_trajectories.png",
    "figure3_detection_ratio_outcomes.svg","figure3_detection_ratio_outcomes.png",
    "figure4_prediction_scorecard.svg","figure4_prediction_scorecard.png",
    "PAPERC_FIGURE_DATA_V1.json"
  ];
  const assets=[];
  for(const name of assetNames){
    const bytes=await fs.readFile(path.join(OUT,name));
    const entry={file:name,sha256:sha(bytes),bytes:bytes.length};
    if(name.endsWith(".png")){const meta=await sharp(bytes).metadata();entry.width=meta.width;entry.height=meta.height;}
    assets.push(entry);
  }
  const manifest={
    schema:"mythos.paperc_figure_manifest.v1",
    status:"REGENERABLE_FROM_FROZEN_RAW",
    source_raw:data.source,
    generator:{file:path.basename(new URL(import.meta.url).pathname),sha256:sha(generatorBytes),bytes:generatorBytes.length},
    assets,
    placements:{
      figure1_instrument_sequence:"Methods 2.7",
      figure2_endpoint_dose_trajectories:"Results 3.1",
      figure3_detection_ratio_outcomes:"Discussion 4.2",
      figure4_prediction_scorecard:"Results 3.6"
    },
    visual_encoding:"Direct labels and line/shape differences accompany color; color is not the sole carrier of meaning."
  };
  await fs.writeFile(path.join(OUT,"PAPERC_FIGURE_MANIFEST_V1.json"),JSON.stringify(manifest,null,2)+"\n");
  return data;
}
