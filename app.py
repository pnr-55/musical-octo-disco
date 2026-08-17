<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>AI Knee Screening | Mathematical Motion Analysis</title>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">

<!-- MediaPipe -->
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/drawing_utils/drawing_utils.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/pose/pose.js"></script>

<style>
:root{
    --bg:#020811;
    --bg2:#061522;
    --blue:#1688ff;
    --cyan:#16ddff;
    --cyan2:#8ef5ff;
    --green:#35efad;
    --yellow:#ffd45c;
    --red:#ff5577;
    --white:#f4fbff;
    --text:#d8e9f2;
    --muted:#7891a4;
    --line:rgba(80,210,255,.14);
    --glass:rgba(5,23,38,.78);
    --radius:20px;
}

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

html{
    scroll-behavior:smooth;
}

body{
    min-height:100vh;
    font-family:"Prompt",sans-serif;
    color:var(--white);
    background:
        radial-gradient(circle at 75% 15%,rgba(0,140,255,.16),transparent 32%),
        radial-gradient(circle at 15% 80%,rgba(0,220,255,.08),transparent 30%),
        linear-gradient(135deg,#020811,#031522 50%,#020a12);
    overflow-x:hidden;
}

button,input{
    font-family:inherit;
}

button{
    cursor:pointer;
}

.background{
    position:fixed;
    inset:0;
    overflow:hidden;
    pointer-events:none;
    z-index:-10;
}

.grid{
    position:absolute;
    width:150%;
    height:150%;
    left:-25%;
    top:-20%;
    background-image:
        linear-gradient(rgba(35,190,255,.045) 1px,transparent 1px),
        linear-gradient(90deg,rgba(35,190,255,.045) 1px,transparent 1px);
    background-size:45px 45px;
    transform:
        perspective(700px)
        rotateX(62deg)
        translateY(120px);
    animation:gridMove 18s linear infinite;
}

@keyframes gridMove{
    from{background-position:0 0,0 0}
    to{background-position:45px 45px,45px 45px}
}

.glow{
    position:absolute;
    border-radius:50%;
    filter:blur(100px);
    opacity:.18;
}

.glow1{
    width:500px;
    height:500px;
    top:-220px;
    right:-180px;
    background:#008cff;
}

.glow2{
    width:400px;
    height:400px;
    bottom:-200px;
    left:-150px;
    background:#00e5ff;
}

.particles{
    position:absolute;
    inset:0;
}

.particle{
    position:absolute;
    width:3px;
    height:3px;
    border-radius:50%;
    background:var(--cyan);
    box-shadow:0 0 12px var(--cyan);
    animation:particle 8s linear infinite;
}

@keyframes particle{
    0%{transform:translateY(30px);opacity:0}
    20%{opacity:.7}
    80%{opacity:.7}
    100%{transform:translateY(-150px);opacity:0}
}

/* ================= HEADER ================= */

.header{
    position:fixed;
    top:0;
    left:0;
    right:0;
    height:76px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding:0 5%;
    background:rgba(2,10,18,.76);
    border-bottom:1px solid var(--line);
    backdrop-filter:blur(20px);
    z-index:1000;
}

.brand{
    display:flex;
    align-items:center;
    gap:12px;
}

.brand-icon{
    width:42px;
    height:42px;
    display:grid;
    place-items:center;
    border-radius:12px;
    font-size:20px;
    font-weight:800;
    background:linear-gradient(135deg,#086dff,#12dfff);
    box-shadow:0 0 25px rgba(19,223,255,.3);
}

.brand-title{
    font-size:14px;
    font-weight:800;
    letter-spacing:1px;
}

.brand-sub{
    margin-top:2px;
    font-size:8px;
    color:#668094;
    letter-spacing:2px;
}

.system-status{
    display:flex;
    align-items:center;
    gap:8px;
    color:#6e8799;
    font-family:"Space Mono",monospace;
    font-size:9px;
    letter-spacing:1px;
}

.status-dot{
    width:7px;
    height:7px;
    border-radius:50%;
    background:var(--green);
    box-shadow:0 0 10px var(--green);
    animation:pulse 1.8s infinite;
}

@keyframes pulse{
    50%{
        transform:scale(1.5);
        opacity:.5;
    }
}

/* ================= GENERAL ================= */

.page{
    display:none;
    min-height:100vh;
    padding-top:76px;
}

.page.active{
    display:block;
    animation:pageIn .45s ease;
}

@keyframes pageIn{
    from{
        opacity:0;
        transform:translateY(12px);
    }
    to{
        opacity:1;
        transform:translateY(0);
    }
}

.container{
    width:min(1180px,92%);
    margin:auto;
}

.btn{
    min-height:48px;
    padding:0 22px;
    border-radius:12px;
    border:1px solid transparent;
    font-size:12px;
    font-weight:700;
    display:inline-flex;
    align-items:center;
    justify-content:center;
    gap:9px;
    transition:.25s;
}

.btn:hover{
    transform:translateY(-3px);
}

.btn-primary{
    color:white;
    background:linear-gradient(135deg,#086dff,#10cfe4);
    box-shadow:0 15px 40px rgba(0,150,255,.2);
}

.btn-primary:hover{
    box-shadow:0 20px 50px rgba(0,180,255,.35);
}

.btn-secondary{
    color:#a5bac9;
    background:rgba(6,25,40,.65);
    border-color:rgba(100,210,255,.15);
}

.btn-secondary:hover{
    color:white;
    border-color:rgba(100,220,255,.4);
}

.page-heading{
    font-size:42px;
    font-weight:800;
}

.page-heading span{
    color:var(--cyan);
}

.page-description{
    margin-top:8px;
    color:var(--muted);
    font-size:13px;
}

/* ================= HOME ================= */

.home{
    width:min(1450px,92%);
    min-height:calc(100vh - 76px);
    margin:auto;
    display:grid;
    grid-template-columns:minmax(0,1fr) minmax(500px,.9fr);
    align-items:center;
    gap:50px;
    padding:50px 0;
}

.eyebrow{
    display:inline-flex;
    align-items:center;
    gap:8px;
    padding:8px 14px;
    border:1px solid rgba(28,222,255,.2);
    border-radius:50px;
    color:#83ecff;
    background:rgba(5,70,100,.14);
    font-size:9px;
    letter-spacing:2px;
}

.eyebrow:before{
    content:"";
    width:6px;
    height:6px;
    border-radius:50%;
    background:var(--cyan);
    box-shadow:0 0 10px var(--cyan);
}

.hero-title{
    margin-top:25px;
    font-size:clamp(50px,6.3vw,92px);
    line-height:.92;
    letter-spacing:-5px;
    font-weight:800;
}

.hero-title .blue{
    display:block;
    background:linear-gradient(90deg,#1688ff,#18ddff,#b4faff);
    -webkit-background-clip:text;
    background-clip:text;
    color:transparent;
}

.hero-title .outline{
    display:block;
    color:transparent;
    -webkit-text-stroke:1px rgba(150,230,255,.38);
}

.hero-description{
    max-width:650px;
    margin-top:25px;
    color:#8da4b5;
    font-size:14px;
    line-height:1.9;
}

.math-strip{
    display:flex;
    flex-wrap:wrap;
    gap:8px;
    margin-top:24px;
}

.math-chip{
    padding:8px 11px;
    color:#9befff;
    background:rgba(4,26,43,.75);
    border:1px solid rgba(53,210,255,.12);
    border-radius:8px;
    font-family:"Space Mono",monospace;
    font-size:9px;
}

.hero-actions{
    display:flex;
    gap:12px;
    margin-top:30px;
}

.mini-data{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    max-width:580px;
    margin-top:38px;
    border:1px solid var(--line);
    border-radius:15px;
    overflow:hidden;
    background:rgba(4,19,31,.58);
}

.mini-card{
    padding:15px;
    border-right:1px solid var(--line);
}

.mini-card:last-child{
    border-right:none;
}

.mini-label{
    color:#587184;
    font-size:8px;
    letter-spacing:1px;
}

.mini-value{
    margin-top:4px;
    color:#dffaff;
    font-family:"Space Mono",monospace;
    font-size:16px;
    font-weight:700;
}

.mini-value span{
    color:#17dcff;
    font-size:9px;
}

/* ================= KNEE VISUAL ================= */

.hero-visual{
    position:relative;
    height:650px;
    display:grid;
    place-items:center;
}

.visual-core{
    position:relative;
    width:520px;
    height:520px;
    display:grid;
    place-items:center;
}

.orbit{
    position:absolute;
    border-radius:50%;
    border:1px solid rgba(25,220,255,.13);
}

.orbit1{
    width:510px;
    height:510px;
    animation:spin 30s linear infinite;
}

.orbit2{
    width:400px;
    height:400px;
    border-style:dashed;
    animation:spinReverse 20s linear infinite;
}

.orbit3{
    width:300px;
    height:300px;
    animation:spin 14s linear infinite;
}

@keyframes spin{
    to{transform:rotate(360deg)}
}

@keyframes spinReverse{
    to{transform:rotate(-360deg)}
}

.orbit-dot{
    position:absolute;
    width:8px;
    height:8px;
    border-radius:50%;
    background:var(--cyan);
    box-shadow:0 0 15px var(--cyan);
}

.dot1{
    top:45px;
    left:50%;
}

.dot2{
    right:20px;
    top:50%;
}

.dot3{
    bottom:40px;
    left:30%;
}

.knee-model{
    position:relative;
    width:290px;
    height:480px;
    animation:float 4s ease-in-out infinite;
}

@keyframes float{
    50%{transform:translateY(-8px)}
}

.bone{
    position:absolute;
    height:10px;
    border-radius:999px;
    transform-origin:left center;
    background:linear-gradient(90deg,#e4fcff,#17dfff);
    box-shadow:0 0 15px rgba(25,220,255,.75);
}

.bone-hip{
    width:90px;
    left:105px;
    top:65px;
}

.bone-thigh{
    width:205px;
    left:145px;
    top:70px;
    transform:rotate(76deg);
    animation:thigh 4s ease-in-out infinite;
}

.bone-shin{
    width:190px;
    left:92px;
    top:250px;
    transform:rotate(112deg);
    animation:shin 4s ease-in-out infinite;
}

@keyframes thigh{
    50%{transform:rotate(91deg)}
}

@keyframes shin{
    50%{transform:rotate(129deg)}
}

.joint{
    position:absolute;
    width:20px;
    height:20px;
    border-radius:50%;
    background:#efffff;
    border:3px solid #16dcff;
    box-shadow:0 0 15px #16dcff,0 0 45px rgba(16,220,255,.45);
    z-index:5;
}

.joint-hip{
    left:96px;
    top:56px;
}

.joint-knee{
    left:63px;
    top:236px;
}

.joint-ankle{
    left:175px;
    top:425px;
}

.scan-line{
    position:absolute;
    width:390px;
    height:2px;
    background:linear-gradient(90deg,transparent,#16e0ff,transparent);
    box-shadow:0 0 12px #16e0ff;
    animation:scan 3.2s ease-in-out infinite;
}

@keyframes scan{
    0%,100%{
        transform:translateY(-190px);
        opacity:0;
    }
    20%{opacity:1}
    75%{
        transform:translateY(190px);
        opacity:1;
    }
}

.angle-display{
    position:absolute;
    width:105px;
    height:105px;
    display:grid;
    place-items:center;
    border-radius:50%;
    background:rgba(2,16,28,.9);
    border:1px solid rgba(30,220,255,.35);
    box-shadow:0 0 45px rgba(0,180,255,.15);
    font-family:"Space Mono",monospace;
    font-size:19px;
    font-weight:700;
    z-index:10;
}

.angle-display:before{
    content:"";
    position:absolute;
    inset:-7px;
    border-radius:50%;
    border:1px dashed rgba(30,220,255,.25);
    animation:spin 8s linear infinite;
}

/* ================= INFORMATION ================= */

.information{
    width:min(1050px,92%);
    margin:auto;
    padding:100px 0 70px;
}

.progress{
    display:flex;
    align-items:center;
    gap:10px;
    margin-top:30px;
    margin-bottom:25px;
}

.progress-step{
    display:flex;
    align-items:center;
    gap:7px;
    color:#587083;
    font-size:9px;
}

.progress-step.active{
    color:#a8f7ff;
}

.progress-number{
    width:28px;
    height:28px;
    display:grid;
    place-items:center;
    border-radius:50%;
    background:rgba(8,35,53,.8);
    border:1px solid var(--line);
    font-family:"Space Mono",monospace;
}

.progress-step.active .progress-number{
    background:linear-gradient(135deg,#087cff,#13dfff);
    color:white;
    border-color:transparent;
}

.progress-line{
    width:45px;
    height:1px;
    background:var(--line);
}

.form-card{
    position:relative;
    padding:32px;
    border:1px solid var(--line);
    border-radius:20px;
    background:linear-gradient(145deg,rgba(8,29,47,.85),rgba(3,16,27,.78));
    backdrop-filter:blur(20px);
    box-shadow:0 30px 80px rgba(0,0,0,.22);
}

.form-title{
    font-size:19px;
    font-weight:700;
}

.form-subtitle{
    margin-top:4px;
    color:#647d90;
    font-size:10px;
}

.form-grid{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:18px;
    margin-top:25px;
}

.field label{
    display:block;
    margin-bottom:7px;
    color:#7890a2;
    font-size:10px;
}

.field input{
    width:100%;
    height:47px;
    padding:0 14px;
    color:white;
    background:rgba(2,14,24,.85);
    border:1px solid rgba(90,190,230,.12);
    border-radius:10px;
    outline:none;
}

.field input:focus{
    border-color:rgba(30,220,255,.55);
    box-shadow:0 0 0 3px rgba(20,210,255,.06);
}

.bmi-box{
    grid-column:1 / -1;
    display:grid;
    grid-template-columns:1fr 1fr 1fr;
    gap:15px;
    margin-top:5px;
    padding:18px;
    border:1px solid rgba(30,220,255,.15);
    border-radius:15px;
    background:linear-gradient(135deg,rgba(0,130,255,.08),rgba(0,220,255,.03));
}

.bmi-main{
    display:flex;
    flex-direction:column;
    justify-content:center;
}

.bmi-label{
    color:#648094;
    font-size:9px;
    letter-spacing:1px;
}

.bmi-value{
    margin-top:5px;
    color:var(--cyan2);
    font-family:"Space Mono",monospace;
    font-size:30px;
    font-weight:700;
}

.bmi-status{
    display:flex;
    align-items:center;
    color:var(--green);
    font-size:13px;
    font-weight:700;
}

.bmi-formula{
    color:#648094;
    font-family:"Space Mono",monospace;
    font-size:9px;
    line-height:1.7;
    display:flex;
    align-items:center;
}

.form-footer{
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:20px;
    margin-top:28px;
    padding-top:20px;
    border-top:1px solid var(--line);
}

.notice{
    color:#5f7789;
    font-size:9px;
    line-height:1.7;
    max-width:560px;
}

/* ================= CAMERA ================= */

.camera-page{
    width:min(1250px,92%);
    margin:auto;
    padding:80px 0;
}

.camera-layout{
    display:grid;
    grid-template-columns:1.4fr .6fr;
    gap:22px;
    margin-top:30px;
}

.camera-panel{
    position:relative;
    min-height:600px;
    overflow:hidden;
    border:1px solid var(--line);
    border-radius:22px;
    background:#020c15;
    box-shadow:0 30px 80px rgba(0,0,0,.3);
}

#videoElement{
    width:100%;
    height:100%;
    min-height:600px;
    display:block;
    object-fit:cover;
    transform:scaleX(-1);
}

#poseCanvas{
    position:absolute;
    inset:0;
    width:100%;
    height:100%;
    pointer-events:none;
    transform:scaleX(-1);
}

.camera-placeholder{
    position:absolute;
    inset:0;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    background:radial-gradient(circle,rgba(0,180,255,.1),transparent 50%);
    z-index:10;
}

.camera-icon{
    width:100px;
    height:100px;
    display:grid;
    place-items:center;
    border:1px solid rgba(30,220,255,.3);
    border-radius:50%;
    font-size:45px;
    box-shadow:0 0 60px rgba(0,200,255,.15);
}

.camera-placeholder h3{
    margin-top:25px;
    font-size:20px;
}

.camera-placeholder p{
    margin-top:7px;
    color:var(--muted);
    font-size:11px;
}

.camera-side{
    padding:24px;
    border:1px solid var(--line);
    border-radius:22px;
    background:var(--glass);
    height:max-content;
}

.metric{
    padding:16px 0;
    border-bottom:1px solid var(--line);
}

.metric:last-child{
    border-bottom:none;
}

.metric-label{
    color:#638095;
    font-size:9px;
}

.metric-value{
    margin-top:5px;
    color:#dffaff;
    font-family:"Space Mono",monospace;
    font-size:22px;
    font-weight:700;
}

.step-button{
    width:100%;
    margin-top:20px;
}

.pose-guide{
    position:absolute;
    left:20px;
    top:20px;
    padding:10px 14px;
    border-radius:10px;
    background:rgba(2,12,22,.78);
    border:1px solid rgba(30,220,255,.25);
    color:#9cefff;
    font-family:"Space Mono",monospace;
    font-size:9px;
    z-index:20;
}

.camera-bottom{
    position:absolute;
    bottom:20px;
    left:20px;
    right:20px;
    display:flex;
    justify-content:space-between;
    gap:15px;
    z-index:20;
}

.camera-live{
    padding:8px 12px;
    border-radius:8px;
    background:rgba(2,10,18,.8);
    border:1px solid rgba(50,240,173,.2);
    color:var(--green);
    font-family:"Space Mono",monospace;
    font-size:9px;
}

/* ================= ANALYSIS ================= */

.analysis-page{
    width:min(1250px,92%);
    margin:auto;
    padding:90px 0;
}

.analysis-grid{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:18px;
    margin-top:30px;
}

.analysis-card{
    padding:25px;
    border:1px solid var(--line);
    border-radius:18px;
    background:var(--glass);
}

.analysis-card h3{
    font-size:12px;
    color:#7591a4;
    letter-spacing:1px;
}

.analysis-number{
    margin-top:12px;
    font-family:"Space Mono",monospace;
    font-size:32px;
    color:var(--cyan2);
}

.bar{
    width:100%;
    height:7px;
    margin-top:15px;
    overflow:hidden;
    border-radius:99px;
    background:#0a2435;
}

.bar span{
    display:block;
    width:0%;
    height:100%;
    border-radius:99px;
    background:linear-gradient(90deg,#087cff,#16ddff);
    transition:width .6s ease;
}

.math-dashboard{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:20px;
    margin-top:22px;
}

.math-card{
    padding:25px;
    border:1px solid var(--line);
    border-radius:18px;
    background:rgba(3,18,30,.82);
}

.math-card h3{
    color:#80eaff;
    font-size:13px;
}

.formula{
    margin-top:15px;
    padding:15px;
    border-radius:12px;
    background:#020c15;
    border:1px solid rgba(50,210,255,.12);
    color:#c8f8ff;
    font-family:"Space Mono",monospace;
    font-size:11px;
    line-height:1.8;
}

.math-values{
    display:grid;
    grid-template-columns:repeat(2,1fr);
    gap:12px;
    margin-top:15px;
}

.math-value{
    padding:14px;
    border-radius:12px;
    background:rgba(8,35,53,.65);
}

.math-value small{
    display:block;
    color:#627b8d;
    font-size:8px;
}

.math-value strong{
    display:block;
    margin-top:5px;
    color:#dffaff;
    font-family:"Space Mono",monospace;
    font-size:18px;
}

/* EXTRA MATHEMATICAL CARDS */

.advanced-math{
    margin-top:22px;
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:15px;
}

.advanced-card{
    padding:20px;
    border:1px solid rgba(30,220,255,.12);
    border-radius:16px;
    background:rgba(3,18,30,.7);
}

.advanced-card .small-title{
    color:#5f7d90;
    font-size:8px;
    letter-spacing:1px;
}

.advanced-card .big-value{
    margin-top:8px;
    color:#bdf8ff;
    font-family:"Space Mono",monospace;
    font-size:21px;
    font-weight:700;
}

.advanced-card .sub{
    margin-top:7px;
    color:#526d80;
    font-size:8px;
}

.score-panel{
    margin-top:22px;
    padding:28px;
    border:1px solid rgba(30,220,255,.16);
    border-radius:20px;
    background:
        linear-gradient(135deg,rgba(0,120,255,.08),rgba(0,220,255,.03));
}

.score-header{
    display:flex;
    justify-content:space-between;
    align-items:center;
}

.score-header h3{
    font-size:14px;
    color:#8cefff;
}

.score-number{
    color:var(--green);
    font-family:"Space Mono",monospace;
    font-size:35px;
    font-weight:700;
}

.score-track{
    height:12px;
    margin-top:18px;
    overflow:hidden;
    border-radius:99px;
    background:#071b29;
}

.score-track span{
    display:block;
    width:0%;
    height:100%;
    border-radius:99px;
    background:linear-gradient(90deg,#087cff,#16ddff,#35efad);
    transition:1s;
}

.score-components{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:10px;
    margin-top:18px;
}

.score-component{
    padding:12px;
    border-radius:10px;
    background:rgba(2,15,25,.6);
}

.score-component small{
    display:block;
    color:#5e7789;
    font-size:8px;
}

.score-component strong{
    display:block;
    margin-top:4px;
    font-family:"Space Mono",monospace;
    color:#dffaff;
}

/* ================= RESULT ================= */

.result-page{
    width:min(1100px,92%);
    margin:auto;
    padding:90px 0;
}

.result-card{
    margin-top:30px;
    padding:35px;
    border:1px solid var(--line);
    border-radius:22px;
    background:var(--glass);
    text-align:center;
}

.result-score{
    font-family:"Space Mono",monospace;
    font-size:70px;
    color:var(--green);
}

.result-title{
    margin-top:5px;
    font-size:25px;
    font-weight:800;
}

.result-warning{
    margin-top:20px;
    padding:15px;
    border-radius:12px;
    background:rgba(255,180,50,.06);
    border:1px solid rgba(255,200,80,.12);
    color:#b6a878;
    font-size:10px;
    line-height:1.8;
}

.result-summary{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:12px;
    margin-top:25px;
}

.summary-box{
    padding:15px;
    border:1px solid var(--line);
    border-radius:12px;
    background:rgba(2,15,25,.6);
}

.summary-box small{
    color:#60798b;
    font-size:8px;
}

.summary-box strong{
    display:block;
    margin-top:5px;
    font-family:"Space Mono",monospace;
    color:#b9f7ff;
}

.result-extra{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:12px;
    margin-top:12px;
}

/* ================= RESPONSIVE ================= */

@media(max-width:1050px){

    .home{
        grid-template-columns:1fr;
        text-align:center;
    }

    .hero-description{
        margin-left:auto;
        margin-right:auto;
    }

    .math-strip,
    .hero-actions{
        justify-content:center;
    }

    .mini-data{
        margin-left:auto;
        margin-right:auto;
    }

    .camera-layout{
        grid-template-columns:1fr;
    }

    .advanced-math{
        grid-template-columns:1fr 1fr;
    }
}

@media(max-width:700px){

    .header{
        padding:0 20px;
    }

    .system-status{
        display:none;
    }

    .hero-title{
        font-size:50px;
    }

    .hero-actions{
        flex-direction:column;
    }

    .btn{
        width:100%;
    }

    .mini-data{
        grid-template-columns:1fr;
    }

    .mini-card{
        border-right:none;
        border-bottom:1px solid var(--line);
    }

    .form-grid{
        grid-template-columns:1fr;
    }

    .bmi-box{
        grid-template-columns:1fr;
    }

    .form-footer{
        flex-direction:column;
        align-items:stretch;
    }

    .analysis-grid,
    .math-dashboard,
    .result-summary,
    .result-extra{
        grid-template-columns:1fr;
    }

    .advanced-math{
        grid-template-columns:1fr;
    }

    .score-components{
        grid-template-columns:1fr 1fr;
    }

    .hero-visual{
        transform:scale(.68);
        height:500px;
    }

    .camera-panel{
        min-height:450px;
    }

    #videoElement{
        min-height:450px;
    }

    #poseCanvas{
        min-height:450px;
    }
}
</style>
</head>

<body>

<div class="background">
    <div class="grid"></div>
    <div class="glow glow1"></div>
    <div class="glow glow2"></div>
    <div class="particles" id="particles"></div>
</div>

<header class="header">

    <div class="brand">
        <div class="brand-icon">K</div>

        <div>
            <div class="brand-title">
                AI KNEE SCREENING
            </div>

            <div class="brand-sub">
                MEDICAL MATHEMATICAL MOTION ANALYSIS
            </div>
        </div>
    </div>

    <div class="system-status">
        <span class="status-dot"></span>
        SYSTEM READY
        <span>•</span>
        AI ENGINE ONLINE
    </div>

</header>


<!-- =========================================================
HOME
========================================================= -->

<section id="homePage" class="page active">

<div class="home">

<div>

<div class="eyebrow">
    AI-ASSISTED BIOMECHANICS
</div>

<h1 class="hero-title">
    KNEE
    <span class="blue">MOTION</span>
    <span class="outline">ANALYSIS</span>
</h1>

<p class="hero-description">
    ระบบต้นแบบสำหรับการคัดกรองสุขภาพข้อเข่าเบื้องต้น
    โดยผสาน Artificial Intelligence, Computer Vision
    และ Mathematical Analysis เพื่อวิเคราะห์รูปแบบ
    การเคลื่อนไหวของข้อเข่าอย่างเป็นระบบ
</p>

<div class="math-strip">

<div class="math-chip">
θ = cos⁻¹((u·v)/|u||v|)
</div>

<div class="math-chip">
v(t) = Δθ/Δt
</div>

<div class="math-chip">
a(t) = Δv/Δt
</div>

<div class="math-chip">
ROM = θmax − θmin
</div>

<div class="math-chip">
σ = √Σ(x−μ)²/n
</div>

<div class="math-chip">
SI = 100 − Δθ/θmax×100
</div>

<div class="math-chip">
BMI = m/h²
</div>

</div>

<div class="hero-actions">

<button id="startBtn" class="btn btn-primary">
เริ่มการประเมิน
<span>→</span>
</button>

<button id="mathBtn" class="btn btn-secondary">
ดู Mathematical Model
</button>

</div>

<div class="mini-data">

<div class="mini-card">
<div class="mini-label">KNEE ANGLE</div>
<div class="mini-value" id="homeAngle">
168.4<span>°</span>
</div>
</div>

<div class="mini-card">
<div class="mini-label">AI CONFIDENCE</div>
<div class="mini-value">
96.2<span>%</span>
</div>
</div>

<div class="mini-card">
<div class="mini-label">MOTION FRAME</div>
<div class="mini-value" id="homeFrame">
0248
</div>
</div>

</div>

</div>


<div class="hero-visual">

<div class="visual-core">

<div class="orbit orbit1">
<div class="orbit-dot dot1"></div>
</div>

<div class="orbit orbit2">
<div class="orbit-dot dot2"></div>
</div>

<div class="orbit orbit3">
<div class="orbit-dot dot3"></div>
</div>

<div class="scan-line"></div>

<div class="knee-model">

<div class="bone bone-hip"></div>
<div class="bone bone-thigh"></div>
<div class="bone bone-shin"></div>

<div class="joint joint-hip"></div>
<div class="joint joint-knee"></div>
<div class="joint joint-ankle"></div>

</div>

<div class="angle-display">
<span id="heroAngle">168.4°</span>
</div>

</div>

</div>

</div>

</section>


<!-- =========================================================
PATIENT INFORMATION
========================================================= -->

<section id="infoPage" class="page">

<div class="information">

<button id="backHomeBtn" class="btn btn-secondary">
← กลับหน้าแรก
</button>

<h2 class="page-heading" style="margin-top:25px">
PATIENT <span>INFORMATION</span>
</h2>

<p class="page-description">
กรุณากรอกข้อมูลเบื้องต้นก่อนเข้าสู่ระบบวิเคราะห์การเคลื่อนไหว
</p>

<div class="progress">

<div class="progress-step active">
<div class="progress-number">01</div>
ข้อมูล
</div>

<div class="progress-line"></div>

<div class="progress-step">
<div class="progress-number">02</div>
AI Camera
</div>

<div class="progress-line"></div>

<div class="progress-step">
<div class="progress-number">03</div>
Analysis
</div>

<div class="progress-line"></div>

<div class="progress-step">
<div class="progress-number">04</div>
Result
</div>

</div>

<div class="form-card">

<div class="form-title">
ข้อมูลผู้เข้ารับการคัดกรอง
</div>

<div class="form-subtitle">
PATIENT PROFILE / BASIC PARAMETERS
</div>

<div class="form-grid">

<div class="field">
<label>ชื่อ</label>
<input id="firstName" type="text" placeholder="กรอกชื่อ">
</div>

<div class="field">
<label>นามสกุล</label>
<input id="lastName" type="text" placeholder="กรอกนามสกุล">
</div>

<div class="field">
<label>อายุ</label>
<input id="age" type="number" min="1" max="120" placeholder="ปี">
</div>

<div class="field">
<label>น้ำหนัก</label>
<input id="weight" type="number" min="1" step="0.1" placeholder="กิโลกรัม">
</div>

<div class="field">
<label>ส่วนสูง</label>
<input id="height" type="number" min="50" step="0.1" placeholder="เซนติเมตร">
</div>

<div class="field">
<label>โรงพยาบาลสำหรับส่งต่อ</label>
<input id="hospital" type="text" placeholder="ชื่อโรงพยาบาล">
</div>

<div class="bmi-box">

<div class="bmi-main">

<div class="bmi-label">
BODY MASS INDEX
</div>

<div id="bmiValue" class="bmi-value">
--.-
</div>

</div>

<div id="bmiStatus" class="bmi-status">
กรุณากรอกน้ำหนักและส่วนสูง
</div>

<div class="bmi-formula">
BMI = น้ำหนัก(kg) ÷ [ส่วนสูง(m)]²
</div>

</div>

</div>

<div class="form-footer">

<div class="notice">

⚠ ระบบนี้เป็นระบบต้นแบบสำหรับ
<b>การคัดกรองเบื้องต้น</b> เท่านั้น
ผลลัพธ์ไม่ถือเป็นการวินิจฉัยโรค
และไม่สามารถใช้แทนการตรวจโดยแพทย์ได้

</div>

<button id="continueBtn" class="btn btn-primary">
ดำเนินการต่อ
<span>→</span>
</button>

</div>

</div>

</div>

</section>


<!-- =========================================================
CAMERA
========================================================= -->

<section id="cameraPage" class="page">

<div class="camera-page">

<button id="cameraBackBtn" class="btn btn-secondary">
← กลับข้อมูลผู้รับการประเมิน
</button>

<h2 class="page-heading" style="margin-top:25px">
AI <span>CAMERA</span>
</h2>

<p class="page-description">
MediaPipe Pose ตรวจจับ Hip • Knee • Ankle และสร้างข้อมูลสำหรับ Mathematical Time-Series Analysis
</p>

<div class="camera-layout">

<div class="camera-panel" id="cameraPanel">

<div class="camera-placeholder" id="cameraPlaceholder">

<div class="camera-icon">
◉
</div>

<h3>
AI Pose Detection
</h3>

<p>
ยืนให้เห็นร่างกายด้านข้างเต็มตัว
</p>

<button id="cameraStartBtn"
class="btn btn-primary"
style="margin-top:25px">
เริ่มกล้อง
</button>

</div>

<div class="pose-guide" id="poseGuide">
WAITING FOR CAMERA
</div>

<div class="camera-bottom">

<div class="camera-live" id="cameraLive">
● CAMERA OFFLINE
</div>

<div class="camera-live">
HIP • KNEE • ANKLE
</div>

</div>

</div>


<div class="camera-side">

<div class="metric">
<div class="metric-label">PATIENT</div>
<div id="cameraPatient" class="metric-value">—</div>
</div>

<div class="metric">
<div class="metric-label">BMI</div>
<div id="cameraBMI" class="metric-value">—</div>
</div>

<div class="metric">
<div class="metric-label">KNEE ANGLE θ</div>
<div id="cameraAngle" class="metric-value">— °</div>
</div>

<div class="metric">
<div class="metric-label">ANGULAR VELOCITY</div>
<div id="cameraVelocity" class="metric-value">— °/s</div>
</div>

<div class="metric">
<div class="metric-label">AI CONFIDENCE</div>
<div id="cameraConfidence" class="metric-value">— %</div>
</div>

<div class="metric">
<div class="metric-label">DETECTION POINTS</div>
<div id="detectionPoints" class="metric-value">0 / 3</div>
</div>

<div class="metric">
<div class="metric-label">FRAME COUNT</div>
<div id="cameraFrame" class="metric-value">0000</div>
</div>

<div class="metric">
<div class="metric-label">STATUS</div>
<div id="cameraStatus"
class="metric-value"
style="color:var(--yellow)">
READY
</div>
</div>

<button id="analysisBtn"
class="btn btn-primary step-button">
เริ่ม Mathematical Analysis →
</button>

</div>

</div>

</div>

</section>


<!-- =========================================================
MATHEMATICAL ANALYSIS
========================================================= -->

<section id="analysisPage" class="page">

<div class="analysis-page">

<button id="analysisBackBtn" class="btn btn-secondary">
← กลับหน้า AI Camera
</button>

<h2 class="page-heading" style="margin-top:25px">
MATHEMATICAL <span>ANALYSIS</span>
</h2>

<p class="page-description">
เปลี่ยนพิกัดจาก AI Pose Detection ให้เป็นตัวแปรทางคณิตศาสตร์
</p>


<!-- TOP METRICS -->

<div class="analysis-grid">

<div class="analysis-card">

<h3>KNEE ANGLE θ</h3>

<div id="analysisAngle"
class="analysis-number">
—°
</div>

<div class="bar">
<span id="angleBar"></span>
</div>

</div>


<div class="analysis-card">

<h3>SYMMETRY INDEX</h3>

<div id="symmetryValue"
class="analysis-number">
—%
</div>

<div class="bar">
<span id="symmetryBar"></span>
</div>

</div>


<div class="analysis-card">

<h3>AI CONFIDENCE</h3>

<div id="confidenceValue"
class="analysis-number">
—%
</div>

<div class="bar">
<span id="confidenceBar"></span>
</div>

</div>

</div>


<!-- MAIN MATH -->

<div class="math-dashboard">


<div class="math-card">

<h3>📐 01 — KNEE ANGLE</h3>

<div class="formula">
θ = cos⁻¹((u · v) / |u||v|)
<br><br>
u = Hip − Knee
<br>
v = Ankle − Knee
<br><br>
ใช้ Dot Product + Euclidean Norm
</div>

<div class="math-values">

<div class="math-value">
<small>ANGLE θ</small>
<strong id="mathAngle">—</strong>
</div>

<div class="math-value">
<small>REFERENCE</small>
<strong>180°</strong>
</div>

</div>

</div>


<div class="math-card">

<h3>⚖️ 02 — SYMMETRY INDEX</h3>

<div class="formula">
Δθ = |θL − θR|
<br><br>
SI = 100 − (Δθ / θmax × 100)
<br><br>
SI → 100% = สมมาตรมาก
</div>

<div class="math-values">

<div class="math-value">
<small>ANGLE DIFFERENCE</small>
<strong id="deltaAngle">—</strong>
</div>

<div class="math-value">
<small>SYMMETRY</small>
<strong id="mathSymmetry">—</strong>
</div>

</div>

</div>


<div class="math-card">

<h3>📈 03 — ANGULAR VELOCITY</h3>

<div class="formula">
ω(t) = dθ/dt
<br><br>
Approximation:
<br>
ω ≈ Δθ / Δt
<br><br>
หน่วย = degrees / second
</div>

<div class="math-values">

<div class="math-value">
<small>VELOCITY</small>
<strong id="mathVelocity">—</strong>
</div>

<div class="math-value">
<small>FRAME</small>
<strong id="mathFrame">—</strong>
</div>

</div>

</div>


<div class="math-card">

<h3>⚡ 04 — ANGULAR ACCELERATION</h3>

<div class="formula">
α(t) = d²θ/dt²
<br><br>
Approximation:
<br>
α ≈ Δω / Δt
<br><br>
หน่วย = degrees / s²
</div>

<div class="math-values">

<div class="math-value">
<small>ACCELERATION</small>
<strong id="mathAcceleration">—</strong>
</div>

<div class="math-value">
<small>Δt</small>
<strong id="mathDeltaTime">—</strong>
</div>

</div>

</div>


<div class="math-card">

<h3>📏 05 — RANGE OF MOTION</h3>

<div class="formula">
ROM = θmax − θmin
<br><br>
วัดช่วงการเคลื่อนไหว
<br>
จากข้อมูลหลาย Frame
</div>

<div class="math-values">

<div class="math-value">
<small>ROM</small>
<strong id="mathROM">—</strong>
</div>

<div class="math-value">
<small>MIN → MAX</small>
<strong id="mathMinMax">—</strong>
</div>

</div>

</div>


<div class="math-card">

<h3>📊 06 — STANDARD DEVIATION</h3>

<div class="formula">
μ = Σx / n
<br><br>
σ = √[Σ(x−μ)² / n]
<br><br>
วัดความแปรปรวนของการเคลื่อนไหว
</div>

<div class="math-values">

<div class="math-value">
<small>MEAN</small>
<strong id="mathMean">—</strong>
</div>

<div class="math-value">
<small>SD</small>
<strong id="mathSD">—</strong>
</div>

</div>

</div>


<div class="math-card">

<h3>⚖️ 07 — BMI</h3>

<div class="formula">
BMI = m / h²
<br><br>
m = body mass (kg)
<br>
h = height (m)
</div>

<div class="math-values">

<div class="math-value">
<small>BMI</small>
<strong id="analysisBMI">—</strong>
</div>

<div class="math-value">
<small>BODY MASS</small>
<strong id="analysisWeight">— kg</strong>
</div>

</div>

</div>


<div class="math-card">

<h3>🤖 08 — AI CONFIDENCE</h3>

<div class="formula">
C = (Cₕ + Cₖ + Cₐ) / 3
<br><br>
Cₕ = Hip visibility
<br>
Cₖ = Knee visibility
<br>
Cₐ = Ankle visibility
</div>

<div class="math-values">

<div class="math-value">
<small>CONFIDENCE</small>
<strong id="mathConfidence">—</strong>
</div>

<div class="math-value">
<small>POINTS</small>
<strong id="mathPoints">—</strong>
</div>

</div>

</div>

</div>


<!-- ADVANCED DATA -->

<div class="advanced-math">

<div class="advanced-card">
<div class="small-title">SAMPLE SIZE</div>
<div id="sampleCount" class="big-value">0</div>
<div class="sub">number of valid frames</div>
</div>

<div class="advanced-card">
<div class="small-title">TIME WINDOW</div>
<div id="timeWindow" class="big-value">0.0 s</div>
<div class="sub">motion observation</div>
</div>

<div class="advanced-card">
<div class="small-title">MAX VELOCITY</div>
<div id="maxVelocity" class="big-value">—</div>
<div class="sub">peak angular velocity</div>
</div>

<div class="advanced-card">
<div class="small-title">MAX ACCELERATION</div>
<div id="maxAcceleration" class="big-value">—</div>
<div class="sub">peak angular acceleration</div>
</div>

</div>


<!-- COMPOSITE SCORE -->

<div class="score-panel">

<div class="score-header">

<h3>
🧠 COMPOSITE MATHEMATICAL SCREENING SCORE
</h3>

<div id="compositeScore"
class="score-number">
—%
</div>

</div>

<div class="score-track">
<span id="compositeBar"></span>
</div>

<div class="score-components">

<div class="score-component">
<small>ANGLE SCORE</small>
<strong id="scoreAngle">—</strong>
</div>

<div class="score-component">
<small>SYMMETRY SCORE</small>
<strong id="scoreSymmetry">—</strong>
</div>

<div class="score-component">
<small>ROM SCORE</small>
<strong id="scoreROM">—</strong>
</div>

<div class="score-component">
<small>AI SCORE</small>
<strong id="scoreAI">—</strong>
</div>

</div>

</div>


<div style="text-align:center;margin-top:35px">

<button id="resultBtn"
class="btn btn-primary">
ประมวลผลผลลัพธ์ →
</button>

</div>

</div>

</section>


<!-- =========================================================
RESULT
========================================================= -->

<section id="resultPage" class="page">

<div class="result-page">

<button id="resultBackBtn" class="btn btn-secondary">
← กลับ Mathematical Analysis
</button>

<div class="result-card">

<div class="bmi-label">
AI-ASSISTED PRELIMINARY SCREENING
</div>

<div id="resultScore"
class="result-score">
—%
</div>

<div id="resultTitle"
class="result-title">
กำลังประมวลผล
</div>


<div class="result-summary">

<div class="summary-box">
<small>BMI</small>
<strong id="resultBMI">—</strong>
</div>

<div class="summary-box">
<small>KNEE ANGLE</small>
<strong id="resultAngle">—</strong>
</div>

<div class="summary-box">
<small>SYMMETRY</small>
<strong id="resultSymmetry">—</strong>
</div>

<div class="summary-box">
<small>AI CONFIDENCE</small>
<strong id="resultConfidence">—</strong>
</div>

</div>


<div class="result-extra">

<div class="summary-box">
<small>ROM</small>
<strong id="resultROM">—</strong>
</div>

<div class="summary-box">
<small>VELOCITY</small>
<strong id="resultVelocity">—</strong>
</div>

<div class="summary-box">
<small>ACCELERATION</small>
<strong id="resultAcceleration">—</strong>
</div>

</div>


<div class="result-warning">

⚠ ผลนี้เป็นเพียงผลการคัดกรองเบื้องต้นจาก
<b>AI Pose Detection + Mathematical Motion Analysis</b>
ไม่ใช่การวินิจฉัยโรค

<br><br>

หากมีอาการปวด บวม ข้อฝืด
หรือความผิดปกติในการเดิน
ควรเข้ารับการประเมินจากบุคลากรทางการแพทย์

</div>


<button id="restartBtn"
class="btn btn-primary"
style="margin-top:25px">
เริ่มการประเมินใหม่
</button>

</div>

</div>

</section>


<script>

document.addEventListener("DOMContentLoaded",function(){

/* =========================================================
PAGE NAVIGATION
========================================================= */

function showPage(pageId){

    document.querySelectorAll(".page").forEach(page=>{
        page.classList.remove("active");
    });

    const target=document.getElementById(pageId);

    if(!target){
        console.error("ไม่พบหน้า:",pageId);
        return;
    }

    target.classList.add("active");

    window.scrollTo({
        top:0,
        behavior:"smooth"
    });
}


/* =========================================================
ELEMENTS
========================================================= */

const startBtn=document.getElementById("startBtn");
const backHomeBtn=document.getElementById("backHomeBtn");
const continueBtn=document.getElementById("continueBtn");
const cameraBackBtn=document.getElementById("cameraBackBtn");
const analysisBtn=document.getElementById("analysisBtn");
const analysisBackBtn=document.getElementById("analysisBackBtn");
const resultBtn=document.getElementById("resultBtn");
const resultBackBtn=document.getElementById("resultBackBtn");
const restartBtn=document.getElementById("restartBtn");


/* =========================================================
NAVIGATION
========================================================= */

startBtn?.addEventListener("click",()=>{
    showPage("infoPage");
});

backHomeBtn?.addEventListener("click",()=>{
    showPage("homePage");
});

cameraBackBtn?.addEventListener("click",()=>{
    showPage("infoPage");
});

analysisBackBtn?.addEventListener("click",()=>{
    showPage("cameraPage");
});

resultBackBtn?.addEventListener("click",()=>{
    showPage("analysisPage");
});


/* =========================================================
BMI
========================================================= */

const weightInput=document.getElementById("weight");
const heightInput=document.getElementById("height");

function calculateBMI(){

    const weight=parseFloat(weightInput?.value);
    const heightCm=parseFloat(heightInput?.value);

    const bmiValue=document.getElementById("bmiValue");
    const bmiStatus=document.getElementById("bmiStatus");

    if(!weight || !heightCm || weight<=0 || heightCm<=0){

        bmiValue.textContent="--.-";

        bmiStatus.textContent=
        "กรุณากรอกน้ำหนักและส่วนสูง";

        bmiStatus.style.color="var(--muted)";

        return null;
    }

    const heightM=heightCm/100;

    const bmi=weight/(heightM*heightM);

    bmiValue.textContent=bmi.toFixed(1);

    let status="";
    let color="";

    /*
      เกณฑ์ตัวอย่างสำหรับการแสดงผลในระบบต้นแบบ
      ไม่ใช่เกณฑ์วินิจฉัยทางการแพทย์
    */

    if(bmi<18.5){
        status="ต่ำกว่าเกณฑ์";
        color="var(--yellow)";
    }
    else if(bmi<23){
        status="อยู่ในเกณฑ์";
        color="var(--green)";
    }
    else if(bmi<25){
        status="เริ่มสูง";
        color="var(--yellow)";
    }
    else if(bmi<30){
        status="สูง";
        color="var(--yellow)";
    }
    else{
        status="สูงมาก";
        color="var(--red)";
    }

    bmiStatus.textContent=status;
    bmiStatus.style.color=color;

    return bmi;
}

weightInput?.addEventListener("input",calculateBMI);
heightInput?.addEventListener("input",calculateBMI);


/* =========================================================
PATIENT DATA
========================================================= */

continueBtn?.addEventListener("click",()=>{

    const firstName=document.getElementById("firstName").value.trim();
    const lastName=document.getElementById("lastName").value.trim();
    const age=document.getElementById("age").value;
    const weight=document.getElementById("weight").value;
    const height=document.getElementById("height").value;
    const hospital=document.getElementById("hospital").value.trim();

    const bmi=calculateBMI();

    if(
        !firstName ||
        !lastName ||
        !age ||
        !weight ||
        !height ||
        !hospital
    ){

        alert("กรุณากรอกข้อมูลให้ครบทุกช่องก่อนดำเนินการต่อ");
        return;
    }

    if(!bmi){

        alert("กรุณาตรวจสอบน้ำหนักและส่วนสูง");
        return;
    }

    const patient={

        firstName:firstName,
        lastName:lastName,

        age:Number(age),

        weight:Number(weight),

        height:Number(height),

        bmi:Number(bmi.toFixed(1)),

        hospital:hospital,

        timestamp:new Date().toISOString()

    };

    sessionStorage.setItem(
        "kneePatient",
        JSON.stringify(patient)
    );

    loadPatient();

    showPage("cameraPage");

});


/* =========================================================
LOAD PATIENT
========================================================= */

function loadPatient(){

    const raw=sessionStorage.getItem("kneePatient");

    if(!raw)return;

    try{

        const patient=JSON.parse(raw);

        const name=
        patient.firstName+" "+patient.lastName;

        document.getElementById("cameraPatient").textContent=name;

        document.getElementById("cameraBMI").textContent=
        patient.bmi;

        document.getElementById("analysisBMI").textContent=
        patient.bmi;

        document.getElementById("analysisWeight").textContent=
        patient.weight+" kg";

        document.getElementById("resultBMI").textContent=
        patient.bmi;

    }catch(error){

        console.error("Patient data error:",error);

    }
}


/* =========================================================
AI CAMERA + MATHEMATICAL DATA
========================================================= */

let videoElement=null;
let canvasElement=null;
let canvasCtx=null;
let pose=null;
let camera=null;

let currentAngle=168.4;

let frameCounter=0;

let previousAngle=null;
let previousVelocity=null;
let previousTimestamp=null;

let currentVelocity=0;
let currentAcceleration=0;

let currentConfidence=0;

let angleHistory=[];
let velocityHistory=[];
let accelerationHistory=[];
let confidenceHistory=[];
let timestampHistory=[];

const cameraStartBtn=
document.getElementById("cameraStartBtn");


/* =========================================================
MATHEMATICAL FUNCTIONS
========================================================= */

/*
    Euclidean Distance

    d = √[(x₂-x₁)² + (y₂-y₁)²]
*/

function distance(A,B){

    if(!A || !B)return null;

    return Math.sqrt(
        Math.pow(A.x-B.x,2)+
        Math.pow(A.y-B.y,2)
    );
}


/*
    Knee Angle

    θ = cos⁻¹((u·v)/|u||v|)
*/

function calculateAngle(A,B,C){

    if(!A || !B || !C)return null;

    const BA={
        x:A.x-B.x,
        y:A.y-B.y
    };

    const BC={
        x:C.x-B.x,
        y:C.y-B.y
    };

    const dot=
        BA.x*BC.x+
        BA.y*BC.y;

    const magBA=
        Math.sqrt(
            BA.x**2+
            BA.y**2
        );

    const magBC=
        Math.sqrt(
            BC.x**2+
            BC.y**2
        );

    if(!magBA || !magBC)return null;

    let value=
        dot/(magBA*magBC);

    value=Math.max(-1,Math.min(1,value));

    return Math.acos(value)*180/Math.PI;
}


/*
    Mean

    μ = Σx/n
*/

function mean(array){

    if(!array.length)return 0;

    return array.reduce(
        (sum,value)=>sum+value,
        0
    )/array.length;
}


/*
    Standard Deviation

    σ = √[Σ(x-μ)²/n]
*/

function standardDeviation(array){

    if(!array.length)return 0;

    const avg=mean(array);

    const variance=
        array.reduce(
            (sum,value)=>{
                return sum+
                    Math.pow(value-avg,2);
            },
            0
        )/array.length;

    return Math.sqrt(variance);
}


/*
    Linear interpolation / clamp
*/

function clamp(value,min,max){

    return Math.max(
        min,
        Math.min(max,value)
    );
}


/* =========================================================
UPDATE POSE METRICS
========================================================= */

function updatePoseMetrics(results){

    if(!results.poseLandmarks){

        document.getElementById("detectionPoints").textContent=
        "0 / 3";

        document.getElementById("cameraConfidence").textContent=
        "0 %";

        currentConfidence=0;

        return;
    }

    const landmarks=results.poseLandmarks;

    /*
        MediaPipe Pose indices

        23 = left hip
        24 = right hip

        25 = left knee
        26 = right knee

        27 = left ankle
        28 = right ankle
    */

    const hipLeft=landmarks[23];
    const hipRight=landmarks[24];

    const kneeLeft=landmarks[25];
    const kneeRight=landmarks[26];

    const ankleLeft=landmarks[27];
    const ankleRight=landmarks[28];


    /*
        เลือกด้านที่มี visibility สูงกว่า
    */

    const candidates=[

        {
            hip:hipLeft,
            knee:kneeLeft,
            ankle:ankleLeft,
            side:"LEFT"
        },

        {
            hip:hipRight,
            knee:kneeRight,
            ankle:ankleRight,
            side:"RIGHT"
        }

    ];


    let best=null;
    let bestConfidence=0;

    candidates.forEach(item=>{

        const h=item.hip?.visibility || 0;
        const k=item.knee?.visibility || 0;
        const a=item.ankle?.visibility || 0;

        const confidence=(h+k+a)/3;

        if(
            confidence>bestConfidence &&
            confidence>.35
        ){

            best=item;
            bestConfidence=confidence;
        }

    });


    /*
        AI Confidence
    */

    currentConfidence=
        clamp(bestConfidence*100,0,100);


    document.getElementById("cameraConfidence").textContent=
        currentConfidence.toFixed(1)+" %";


    document.getElementById("mathConfidence").textContent=
        currentConfidence.toFixed(1)+" %";


    confidenceHistory.push(
        currentConfidence
    );


    /*
        Detection Points
    */

    if(!best){

        document.getElementById("detectionPoints").textContent=
        "0 / 3";

        return;
    }


    const visiblePoints=[
        best.hip,
        best.knee,
        best.ankle
    ].filter(
        p=>p && p.visibility>.45
    ).length;


    document.getElementById("detectionPoints").textContent=
        visiblePoints+" / 3";


    /*
        Calculate Knee Angle
    */

    if(visiblePoints===3){

        const angle=
            calculateAngle(
                best.hip,
                best.knee,
                best.ankle
            );

        if(angle!==null){

            currentAngle=angle;

            /*
                Timestamp
            */

            const now=
                performance.now()/1000;

            /*
                Angular Velocity

                ω ≈ Δθ / Δt
            */

            if(
                previousAngle!==null &&
                previousTimestamp!==null
            ){

                const dt=
                    now-previousTimestamp;

                if(dt>0.001 && dt<1){

                    currentVelocity=
                        (angle-previousAngle)/dt;

                    velocityHistory.push(
                        currentVelocity
                    );

                    /*
                        Angular Acceleration

                        α ≈ Δω / Δt
                    */

                    if(previousVelocity!==null){

                        currentAcceleration=
                            (currentVelocity-
                             previousVelocity)/dt;

                        accelerationHistory.push(
                            currentAcceleration
                        );

                    }

                }

            }


            previousAngle=angle;
            previousVelocity=currentVelocity;
            previousTimestamp=now;


            /*
                Store Time Series
            */

            angleHistory.push(angle);

            timestampHistory.push(now);


            /*
                จำกัด memory
                ป้องกันข้อมูลเยอะเกิน
            */

            if(angleHistory.length>1000){

                angleHistory.shift();
            }

            if(velocityHistory.length>1000){

                velocityHistory.shift();
            }

            if(accelerationHistory.length>1000){

                accelerationHistory.shift();
            }

            if(confidenceHistory.length>1000){

                confidenceHistory.shift();
            }

            if(timestampHistory.length>1000){

                timestampHistory.shift();
            }


            /*
                Update UI
            */

            document.getElementById("cameraAngle").textContent=
                angle.toFixed(1)+" °";

            document.getElementById("cameraVelocity").textContent=
                Math.abs(currentVelocity).toFixed(1)+" °/s";


            document.getElementById("poseGuide").textContent=
                "POSE LOCKED • AI TRACKING";


            document.getElementById("cameraStatus").textContent=
                "AI TRACKING";


            document.getElementById("cameraStatus").style.color=
                "var(--green)";

        }

    }else{

        document.getElementById("poseGuide").textContent=
            "MOVE INTO FRAME";

    }

}


/* =========================================================
POSE DRAW
========================================================= */

function onPoseResults(results){

    if(!canvasCtx)return;

    canvasCtx.clearRect(
        0,
        0,
        canvasElement.width,
        canvasElement.height
    );


    if(results.poseLandmarks){

        drawConnectors(
            canvasCtx,
            results.poseLandmarks,
            POSE_CONNECTIONS,
            {
                color:"#16ddff",
                lineWidth:4
            }
        );

        drawLandmarks(
            canvasCtx,
            results.poseLandmarks,
            {
                color:"#ffffff",
                fillColor:"#1688ff",
                lineWidth:2,
                radius:5
            }
        );

    }

    updatePoseMetrics(results);
}


/* =========================================================
START CAMERA
========================================================= */

async function startCamera(){

    if(
        !navigator.mediaDevices ||
        !navigator.mediaDevices.getUserMedia
    ){

        alert(
            "Browser นี้ไม่รองรับการใช้งานกล้อง"
        );

        return;
    }


    /*
        Reset motion arrays
    */

    frameCounter=0;

    previousAngle=null;
    previousVelocity=null;
    previousTimestamp=null;

    currentVelocity=0;
    currentAcceleration=0;

    angleHistory=[];
    velocityHistory=[];
    accelerationHistory=[];
    confidenceHistory=[];
    timestampHistory=[];


    try{

        videoElement=
            document.createElement("video");

        videoElement.id="videoElement";

        videoElement.autoplay=true;
        videoElement.playsInline=true;

        canvasElement=
            document.createElement("canvas");

        canvasElement.id="poseCanvas";


        const panel=
            document.getElementById("cameraPanel");


        const placeholder=
            document.getElementById("cameraPlaceholder");


        placeholder.style.display="none";


        /*
            Remove old camera
            if user starts again
        */

        const oldVideo=
            panel.querySelector("#videoElement");

        const oldCanvas=
            panel.querySelector("#poseCanvas");

        if(oldVideo)oldVideo.remove();
        if(oldCanvas)oldCanvas.remove();


        panel.appendChild(videoElement);
        panel.appendChild(canvasElement);


        canvasCtx=
            canvasElement.getContext("2d");


        /*
            MediaPipe Pose
        */

        pose=new Pose({

            locateFile:(file)=>{

                return `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`;

            }

        });


        pose.setOptions({

            modelComplexity:1,

            smoothLandmarks:true,

            enableSegmentation:false,

            smoothSegmentation:false,

            minDetectionConfidence:.55,

            minTrackingConfidence:.55

        });


        pose.onResults(onPoseResults);


        /*
            MediaPipe Camera
        */

        camera=new Camera(

            videoElement,

            {

                onFrame:async()=>{

                    canvasElement.width=
                        videoElement.videoWidth ||
                        640;

                    canvasElement.height=
                        videoElement.videoHeight ||
                        480;


                    frameCounter++;


                    document.getElementById(
                        "cameraFrame"
                    ).textContent=
                        String(frameCounter)
                        .padStart(4,"0");


                    await pose.send({
                        image:videoElement
                    });

                },

                width:640,

                height:480

            }

        );


        await camera.start();


        document.getElementById("cameraLive").textContent=
            "● CAMERA ONLINE";

        document.getElementById("cameraLive").style.color=
            "var(--green)";


        document.getElementById("cameraStatus").textContent=
            "AI ONLINE";

        document.getElementById("cameraStatus").style.color=
            "var(--green)";


    }catch(error){

        console.error(error);

        alert(
            "ไม่สามารถเปิดกล้องได้ กรุณาอนุญาตการเข้าถึงกล้อง"
        );


        document.getElementById("cameraStatus").textContent=
            "CAMERA ERROR";

        document.getElementById("cameraStatus").style.color=
            "var(--red)";

    }

}


cameraStartBtn?.addEventListener(
    "click",
    startCamera
);


/* =========================================================
CALCULATE MATHEMATICAL ANALYSIS
========================================================= */

function calculateAnalysis(){

    /*
        ถ้าไม่มีข้อมูลจากกล้อง
        ใช้ข้อมูลเริ่มต้นสำหรับ demo
    */

    const angles=
        angleHistory.length
        ? angleHistory
        : [currentAngle];


    const velocities=
        velocityHistory.length
        ? velocityHistory
        : [0];


    const accelerations=
        accelerationHistory.length
        ? accelerationHistory
        : [0];


    const avgAngle=
        mean(angles);


    const minAngle=
        Math.min(...angles);


    const maxAngle=
        Math.max(...angles);


    /*
        ROM

        ROM = θmax - θmin
    */

    const rom=
        maxAngle-minAngle;


    /*
        Standard Deviation
    */

    const sd=
        standardDeviation(angles);


    /*
        Velocity
    */

    const avgVelocity=
        mean(
            velocities.map(v=>Math.abs(v))
        );


    const maxVelocity=
        Math.max(
            ...velocities.map(
                v=>Math.abs(v)
            )
        );


    /*
        Acceleration
    */

    const avgAcceleration=
        mean(
            accelerations.map(
                a=>Math.abs(a)
            )
        );


    const maxAcceleration=
        Math.max(
            ...accelerations.map(
                a=>Math.abs(a)
            )
        );


    /*
        AI Confidence
    */

    const aiConfidence=
        confidenceHistory.length
        ? mean(confidenceHistory)
        : 0;


    /*
        Symmetry

        เนื่องจากการเลือกด้านที่ดีที่สุดในกล้อง
        ระบบ prototype ใช้ deviation
        จาก reference angle เป็นตัวแทน

        หากมีข้อมูลซ้าย/ขวาในอนาคต
        สามารถเปลี่ยนเป็น |θL-θR| ได้โดยตรง
    */

    const referenceAngle=168.4;

    const deltaAngle=
        Math.abs(
            avgAngle-referenceAngle
        );


    const symmetry=
        clamp(
            100-
            (deltaAngle/180*100),
            0,
            100
        );


    /*
        ANGLE SCORE

        ใกล้ reference → score สูง
    */

    const angleScore=
        clamp(
            100-
            Math.abs(
                avgAngle-referenceAngle
            )*2,
            0,
            100
        );


    /*
        ROM SCORE

        เป็นคะแนนเชิงต้นแบบ
        ไม่ใช่เกณฑ์วินิจฉัย
    */

    const romScore=
        clamp(
            100-
            Math.abs(
                rom-30
            )*1.5,
            0,
            100
        );


    /*
        Composite Score

        35% Angle
        30% Symmetry
        20% ROM
        15% AI Confidence
    */

    const composite=
        (
            angleScore*.35+
            symmetry*.30+
            romScore*.20+
            aiConfidence*.15
        );


    return{

        avgAngle,
        minAngle,
        maxAngle,
        rom,

        sd,

        avgVelocity,
        maxVelocity,

        avgAcceleration,
        maxAcceleration,

        aiConfidence,

        deltaAngle,
        symmetry,

        angleScore,
        romScore,

        composite

    };

}


/* =========================================================
DISPLAY ANALYSIS
========================================================= */

analysisBtn?.addEventListener(
"click",
()=>{

    const data=
        calculateAnalysis();


    /*
        Basic metrics
    */

    document.getElementById(
        "analysisAngle"
    ).textContent=
        data.avgAngle.toFixed(1)+"°";


    document.getElementById(
        "mathAngle"
    ).textContent=
        data.avgAngle.toFixed(1)+"°";


    document.getElementById(
        "angleBar"
    ).style.width=
        clamp(
            data.avgAngle/1.8,
            0,
            100
        )+"%";


    /*
        Symmetry
    */

    document.getElementById(
        "symmetryValue"
    ).textContent=
        data.symmetry.toFixed(1)+"%";


    document.getElementById(
        "mathSymmetry"
    ).textContent=
        data.symmetry.toFixed(1)+"%";


    document.getElementById(
        "symmetryBar"
    ).style.width=
        data.symmetry+"%";


    document.getElementById(
        "deltaAngle"
    ).textContent=
        data.deltaAngle.toFixed(1)+"°";


    /*
        Confidence
    */

    document.getElementById(
        "confidenceValue"
    ).textContent=
        data.aiConfidence.toFixed(1)+"%";


    document.getElementById(
        "mathConfidence"
    ).textContent=
        data.aiConfidence.toFixed(1)+"%";


    document.getElementById(
        "confidenceBar"
    ).style.width=
        data.aiConfidence+"%";


    /*
        Velocity
    */

    document.getElementById(
        "mathVelocity"
    ).textContent=
        data.avgVelocity.toFixed(2)+"°/s";


    /*
        Acceleration
    */

    document.getElementById(
        "mathAcceleration"
    ).textContent=
        data.avgAcceleration.toFixed(2)+"°/s²";


    /*
        Delta time
    */

    let totalTime=0;

    if(timestampHistory.length>=2){

        totalTime=
            timestampHistory[
                timestampHistory.length-1
            ]-
            timestampHistory[0];

    }


    document.getElementById(
        "mathDeltaTime"
    ).textContent=
        totalTime.toFixed(2)+" s";


    /*
        ROM
    */

    document.getElementById(
        "mathROM"
    ).textContent=
        data.rom.toFixed(2)+"°";


    document.getElementById(
        "mathMinMax"
    ).textContent=
        data.minAngle.toFixed(1)+
        " → "+
        data.maxAngle.toFixed(1)+"°";


    /*
        Mean / SD
    */

    document.getElementById(
        "mathMean"
    ).textContent=
        data.avgAngle.toFixed(2)+"°";


    document.getElementById(
        "mathSD"
    ).textContent=
        data.sd.toFixed(2)+"°";


    /*
        Frame
    */

    document.getElementById(
        "mathFrame"
    ).textContent=
        String(frameCounter)
        .padStart(4,"0");


    document.getElementById(
        "mathPoints"
    ).textContent=
        "3 / 3";


    /*
        Advanced
    */

    document.getElementById(
        "sampleCount"
    ).textContent=
        anglesLength();


    document.getElementById(
        "timeWindow"
    ).textContent=
        totalTime.toFixed(2)+" s";


    document.getElementById(
        "maxVelocity"
    ).textContent=
        data.maxVelocity.toFixed(2)+"°/s";


    document.getElementById(
        "maxAcceleration"
    ).textContent=
        data.maxAcceleration.toFixed(2)+"°/s²";


    /*
        Composite
    */

    document.getElementById(
        "compositeScore"
    ).textContent=
        data.composite.toFixed(1)+"%";


    document.getElementById(
        "compositeBar"
    ).style.width=
        data.composite+"%";


    document.getElementById(
        "scoreAngle"
    ).textContent=
        data.angleScore.toFixed(1)+"%";


    document.getElementById(
        "scoreSymmetry"
    ).textContent=
        data.symmetry.toFixed(1)+"%";


    document.getElementById(
        "scoreROM"
    ).textContent=
        data.romScore.toFixed(1)+"%";


    document.getElementById(
        "scoreAI"
    ).textContent=
        data.aiConfidence.toFixed(1)+"%";


    /*
        Save latest analysis
    */

    sessionStorage.setItem(
        "kneeAnalysis",
        JSON.stringify(data)
    );


    showPage("analysisPage");

});


function anglesLength(){

    return angleHistory.length || 1;

}


/* =========================================================
RESULT
========================================================= */

resultBtn?.addEventListener(
"click",
()=>{

    const raw=
        sessionStorage.getItem(
            "kneeAnalysis"
        );


    const data=
        raw
        ? JSON.parse(raw)
        : calculateAnalysis();


    /*
        Score
    */

    document.getElementById(
        "resultScore"
    ).textContent=
        data.composite.toFixed(1)+"%";


    /*
        Angle
    */

    document.getElementById(
        "resultAngle"
    ).textContent=
        data.avgAngle.toFixed(1)+"°";


    /*
        Symmetry
    */

    document.getElementById(
        "resultSymmetry"
    ).textContent=
        data.symmetry.toFixed(1)+"%";


    /*
        Confidence
    */

    document.getElementById(
        "resultConfidence"
    ).textContent=
        data.aiConfidence.toFixed(1)+"%";


    /*
        ROM
    */

    document.getElementById(
        "resultROM"
    ).textContent=
        data.rom.toFixed(1)+"°";


    /*
        Velocity
    */

    document.getElementById(
        "resultVelocity"
    ).textContent=
        data.avgVelocity.toFixed(1)+"°/s";


    /*
        Acceleration
    */

    document.getElementById(
        "resultAcceleration"
    ).textContent=
        data.avgAcceleration.toFixed(1)+"°/s²";


    /*
        Result interpretation
    */

    const title=
        document.getElementById(
            "resultTitle"
        );

    const score=
        document.getElementById(
            "resultScore"
        );


    if(data.composite>=85){

        title.textContent=
        "รูปแบบการเคลื่อนไหวอยู่ในระดับดีจากการคัดกรองเบื้องต้น";

        score.style.color=
            "var(--green)";

    }
    else if(data.composite>=70){

        title.textContent=
        "พบค่าความแตกต่างบางส่วน ควรติดตามการเคลื่อนไหว";

        score.style.color=
            "var(--yellow)";

    }
    else{

        title.textContent=
        "พบค่าที่ควรประเมินเพิ่มเติมโดยบุคลากรทางการแพทย์";

        score.style.color=
            "var(--red)";

    }


    showPage("resultPage");

});


/* =========================================================
RESTART
========================================================= */

restartBtn?.addEventListener(
"click",
()=>{

    if(camera){

        try{
            camera.stop();
        }
        catch(e){
            console.warn(e);
        }

    }


    /*
        Reset data
    */

    sessionStorage.removeItem(
        "kneePatient"
    );

    sessionStorage.removeItem(
        "kneeAnalysis"
    );


    angleHistory=[];
    velocityHistory=[];
    accelerationHistory=[];
    confidenceHistory=[];
    timestampHistory=[];


    previousAngle=null;
    previousVelocity=null;
    previousTimestamp=null;


    currentVelocity=0;
    currentAcceleration=0;

    frameCounter=0;


    /*
        Reset form
    */

    [
        "firstName",
        "lastName",
        "age",
        "weight",
        "height",
        "hospital"
    ].forEach(id=>{

        const element=
            document.getElementById(id);

        if(element){

            element.value="";

        }

    });


    document.getElementById(
        "bmiValue"
    ).textContent=
        "--.-";


    document.getElementById(
        "bmiStatus"
    ).textContent=
        "กรุณากรอกน้ำหนักและส่วนสูง";


    document.getElementById(
        "bmiStatus"
    ).style.color=
        "var(--muted)";


    /*
        Remove video
    */

    const oldVideo=
        document.getElementById(
            "videoElement"
        );

    const oldCanvas=
        document.getElementById(
            "poseCanvas"
        );


    oldVideo?.remove();
    oldCanvas?.remove();


    document.getElementById(
        "cameraPlaceholder"
    ).style.display=
        "flex";


    document.getElementById(
        "cameraLive"
    ).textContent=
        "● CAMERA OFFLINE";


    document.getElementById(
        "cameraStatus"
    ).textContent=
        "READY";


    document.getElementById(
        "cameraStatus"
    ).style.color=
        "var(--yellow)";


    document.getElementById(
        "cameraFrame"
    ).textContent=
        "0000";


    showPage("infoPage");

});


/* =========================================================
MATH BUTTON
========================================================= */

document.getElementById(
    "mathBtn"
)?.addEventListener(
"click",
()=>{

    document
        .querySelector(".math-strip")
        .scrollIntoView({
            behavior:"smooth",
            block:"center"
        });

});


/* =========================================================
PARTICLES
========================================================= */

const particleContainer=
    document.getElementById(
        "particles"
    );


for(let i=0;i<45;i++){

    const particle=
        document.createElement("span");

    particle.className=
        "particle";

    particle.style.left=
        Math.random()*100+"%";

    particle.style.top=
        Math.random()*100+"%";

    particle.style.animationDuration=
        (5+Math.random()*8)+"s";

    particle.style.animationDelay=
        (-Math.random()*8)+"s";

    particleContainer.appendChild(
        particle
    );

}


/* =========================================================
HOME LIVE DEMO
========================================================= */

let frame=248;

function motionDemo(){

    const time=
        performance.now()/1000;


    const angle=
        164+
        Math.sin(time*1.4)*6;


    document.getElementById(
        "heroAngle"
    ).textContent=
        angle.toFixed(1)+"°";


    document.getElementById(
        "homeAngle"
    ).innerHTML=
        angle.toFixed(1)+
        "<span>°</span>";


    frame++;


    if(frame>9999){
        frame=0;
    }


    document.getElementById(
        "homeFrame"
    ).textContent=
        String(frame)
        .padStart(4,"0");


    requestAnimationFrame(
        motionDemo
    );

}

motionDemo();


/* =========================================================
INITIALIZE
========================================================= */

calculateBMI();

loadPatient();

});
</script>

</body>
</html>

	
Pause mobile notifications while you're using this device
To pause Chat mobile notifications while you’re active on this device, allow your browser to detect if you’re active or away. Click Continue and then Allow when prompted by your browser.
