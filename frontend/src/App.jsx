/* eslint-disable no-unused-vars */
import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
} from "recharts";
import {
  Activity,
  Upload,
  Share2,
  Info,
  CheckCircle2,
  AlertTriangle,
  TrendingUp,
  AlertCircle,
  ImageIcon,
  FileText,
  UploadCloud,
  X,
  Loader,
  AlertCircle as AlertIcon,
} from "lucide-react";

// --- API CONFIGURATION ---
const API_BASE_URL = "http://localhost:5000";

// --- DEFAULT DATA ---
const DEFAULT_DATA = {
  patient_id: "patient_000",
  current_day: 0,
  metrics: {
    healing_score: 0,
    status: "Improving ↑",
    redness: 0,
    wound_area: 0,
    infection_risk_pct: 0,
    risk_level: "Medium",
    contributing_factors: ["Wound area growing"],
  },
  chartData: [
    { day: 1, score: 50, redness: 0.8, area: 1000 },
    { day: 2, score: 62, redness: 0.6, area: 1050 },
    { day: 3, score: 72.5, redness: 0.45, area: 1200 },
  ],
  ai_report: {
    doctor_summary:
      "Patient_001's wound healing score has improved to 72.5/100 on day 3, with a reducing redness level of 0.45 and an infection risk at medium (35%). However, there is a concern as the wound area is growing. Continue monitoring and consider adjusting treatment plan if necessary.",
    patient_advice: [
      "Maintain current wound care regimen",
      "Monitor wound area closely",
      "Consult with healthcare provider for potential treatment adjustments",
    ],
  },
};

// --- SHADCN/UI MOCK COMPONENTS ---

const Card = ({ children, className = "" }) => (
  <div
    className={`rounded-xl border border-slate-200 bg-white text-slate-950 shadow-sm ${className}`}
  >
    {children}
  </div>
);

const CardHeader = ({ children, className = "" }) => (
  <div className={`flex flex-col space-y-1.5 p-6 ${className}`}>{children}</div>
);

const CardTitle = ({ children, className = "" }) => (
  <h3 className={`font-semibold leading-none tracking-tight ${className}`}>
    {children}
  </h3>
);

const CardContent = ({ children, className = "" }) => (
  <div className={`p-6 pt-0 ${className}`}>{children}</div>
);

const Badge = ({ children, variant = "default", className = "" }) => {
  const variants = {
    default:
      "border-transparent bg-slate-900 text-slate-50 hover:bg-slate-900/80",
    success:
      "border-transparent bg-emerald-100 text-emerald-800 hover:bg-emerald-100/80",
    warning:
      "border-transparent bg-amber-100 text-amber-800 hover:bg-amber-100/80",
    destructive:
      "border-transparent bg-rose-100 text-rose-800 hover:bg-rose-100/80",
    outline: "text-slate-950 border-slate-200",
  };
  return (
    <div
      className={`inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-slate-950 focus:ring-offset-2 ${variants[variant]} ${className}`}
    >
      {children}
    </div>
  );
};

const Progress = ({
  value,
  className = "",
  indicatorClass = "bg-slate-900",
}) => (
  <div
    className={`relative h-2 w-full overflow-hidden rounded-full bg-slate-100 ${className}`}
  >
    <div
      className={`h-full w-full flex-1 transition-all duration-500 ease-in-out ${indicatorClass}`}
      style={{ transform: `translateX(-${100 - (value || 0)}%)` }}
    />
  </div>
);

const Button = ({
  children,
  variant = "default",
  size = "default",
  className = "",
  ...props
}) => {
  const variants = {
    default: "bg-slate-900 text-slate-50 hover:bg-slate-900/90",
    outline:
      "border border-slate-200 bg-white hover:bg-slate-100 hover:text-slate-900",
    ghost: "hover:bg-slate-100 hover:text-slate-900",
  };
  const sizes = {
    default: "h-9 px-4 py-2",
    sm: "h-8 rounded-md px-3 text-xs",
    icon: "h-9 w-9 flex items-center justify-center",
  };
  return (
    <button
      className={`inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-slate-950 disabled:pointer-events-none disabled:opacity-50 ${variants[variant]} ${sizes[size]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
};

const SimpleTooltip = ({ children, text }) => (
  <div className="group relative flex items-center justify-center">
    {children}
    <div className="absolute bottom-full mb-2 hidden group-hover:block w-max max-w-xs px-2 py-1 bg-slate-800 text-slate-50 text-xs rounded shadow-md z-50 pointer-events-none">
      {text}
      <div className="absolute top-full left-1/2 -translate-x-1/2 border-4 border-transparent border-t-slate-800" />
    </div>
  </div>
);

// --- DASHBOARD SECTIONS ---

const Header = ({ onUploadClick, patientData }) => {
  const [isCopied, setIsCopied] = useState(false);

  const handleShare = () => {
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(window.location.href);
    } else {
      const textArea = document.createElement("textarea");
      textArea.value = window.location.href;
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();
      try {
        document.execCommand("copy");
      } catch (err) {
        console.error("Unable to copy", err);
      }
      document.body.removeChild(textArea);
    }

    setIsCopied(true);
    setTimeout(() => setIsCopied(false), 2000);
  };

  return (
    <header className="flex flex-col sm:flex-row items-start sm:items-center justify-between pb-6 mb-6 border-b border-slate-200 gap-4">
      <div>
        <div className="flex items-center gap-2 mb-1">
          <div className="p-2 bg-emerald-100 rounded-lg">
            <Activity className="w-5 h-5 text-emerald-600" />
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">
            HealTrack AI
          </h1>
        </div>
        <p className="text-sm text-slate-500 font-medium">
          Patient:{" "}
          <span className="text-slate-900">{patientData.patient_id}</span> • Day{" "}
          {patientData.current_day} of Assessment
        </p>
      </div>
      <div className="flex items-center gap-2 w-full sm:w-auto">
        <Button
          variant="outline"
          className="w-full sm:w-auto"
          onClick={handleShare}
        >
          {isCopied ? (
            <CheckCircle2 className="w-4 h-4 mr-2 text-emerald-500" />
          ) : (
            <Share2 className="w-4 h-4 mr-2" />
          )}
          {isCopied ? "Copied Link!" : "Share Report"}
        </Button>
        <Button className="w-full sm:w-auto" onClick={onUploadClick}>
          <Upload className="w-4 h-4 mr-2" /> Upload Scan
        </Button>
      </div>
    </header>
  );
};

const MetricsBanner = ({ metrics }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium text-slate-500">
            Healing Score
          </CardTitle>
          <SimpleTooltip text="Composite score based on area, redness, and granulation tissue.">
            <Info className="h-4 w-4 text-slate-400" />
          </SimpleTooltip>
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold mb-2">
            {metrics.healing_score}{" "}
            <span className="text-sm font-normal text-slate-500">/ 100</span>
          </div>
          <Progress
            value={metrics.healing_score}
            indicatorClass="bg-emerald-500"
          />
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium text-slate-500">
            Current Status
          </CardTitle>
          <TrendingUp className="h-4 w-4 text-slate-400" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold mb-2">
            {metrics.status.split(" ")[0]}
          </div>
          <Badge variant="success" className="bg-emerald-100 text-emerald-800">
            {metrics.status}
          </Badge>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium text-slate-500">
            Infection Risk
          </CardTitle>
          <SimpleTooltip text="AI prediction based on thermal imaging and redness expansion patterns.">
            <AlertTriangle className="h-4 w-4 text-slate-400" />
          </SimpleTooltip>
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold mb-2">
            {metrics.infection_risk_pct}%
          </div>
          <Badge variant="warning">{metrics.risk_level} Risk</Badge>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium text-slate-500">
            Recent Flags
          </CardTitle>
          <AlertCircle className="h-4 w-4 text-rose-400" />
        </CardHeader>
        <CardContent>
          <div className="text-lg font-semibold text-rose-600 mt-1">
            {metrics.contributing_factors[0] || "No flags"}
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Requires attention during next dressing change.
          </p>
        </CardContent>
      </Card>
    </div>
  );
};

const VisualAnalysis = () => {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <ImageIcon className="w-5 h-5 text-slate-500" />
            Healing Timeline
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center gap-4 overflow-x-auto pb-4 snap-x">
            {[1, 2, 3].map((day, i) => (
              <motion.div
                key={day}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.1 }}
                className="shrink-0 w-32 snap-start"
              >
                <div className="aspect-square rounded-lg bg-slate-100 border-2 border-slate-200 overflow-hidden relative mb-2 flex items-center justify-center">
                  <div
                    className={`w-16 h-16 rounded-full opacity-50 blur-md transition-all ${day === 3 ? "bg-rose-300 scale-110" : "bg-emerald-200"}`}
                  />
                  <span className="absolute bottom-1 right-2 text-[10px] font-mono text-slate-400">
                    IMG_{day}
                  </span>
                </div>
                <div className="text-center text-sm font-medium">Day {day}</div>
              </motion.div>
            ))}
          </div>
        </CardContent>
      </Card>

      <Card className="border-emerald-200 shadow-sm relative overflow-hidden">
        <div className="absolute top-0 right-0 p-4">
          <Badge variant="success" className="animate-pulse">
            AI Active
          </Badge>
        </div>
        <CardHeader>
          <CardTitle className="text-emerald-800">
            Future Wound Simulation
          </CardTitle>
          <p className="text-sm text-slate-500">
            Predictive modeling for Day 4+ based on current trajectory.
          </p>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1">
              <div className="text-xs font-semibold text-slate-500 mb-2 uppercase tracking-wider">
                Current (Day 3)
              </div>
              <div className="aspect-video rounded-lg bg-slate-100 border border-slate-200 relative overflow-hidden flex items-center justify-center">
                <div className="w-24 h-24 rounded-[40%] bg-rose-200/80 blur-sm mix-blend-multiply" />
                <div className="absolute inset-0 bg-grid-slate-200/[0.04] bg-size-[16px_16px]" />
              </div>
            </div>

            <div className="flex-1 relative">
              <div className="text-xs font-semibold text-emerald-600 mb-2 uppercase tracking-wider">
                Predicted (Day 4)
              </div>
              <div className="aspect-video rounded-lg bg-slate-900 border border-slate-800 relative overflow-hidden flex items-center justify-center">
                <motion.div
                  initial={{ scale: 1.1 }}
                  animate={{ scale: 1 }}
                  transition={{
                    duration: 2,
                    repeat: Infinity,
                    repeatType: "reverse",
                  }}
                  className="w-20 h-20 rounded-[50%] bg-emerald-400/40 blur-md mix-blend-screen"
                />

                <motion.div
                  animate={{ top: ["-10%", "110%", "-10%"] }}
                  transition={{ duration: 4, repeat: Infinity, ease: "linear" }}
                  className="absolute left-0 right-0 h-1 bg-emerald-400/80 shadow-[0_0_15px_3px_rgba(52,211,153,0.5)] z-10"
                />
                <div className="absolute inset-0 bg-grid-white/[0.05] bg-size-[16px_16px]" />
                <span className="absolute bottom-2 left-2 text-[10px] font-mono text-emerald-500/50 z-20">
                  SIM_V2.1_RUNNING
                </span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-white p-2 rounded border border-slate-200 shadow-lg">
        <p className="text-xs font-medium text-slate-900">{`Day ${label}`}</p>
        {payload.map((entry, index) => (
          <p key={index} style={{ color: entry.color }} className="text-xs">
            {`${entry.name}: ${entry.value}`}
          </p>
        ))}
      </div>
    );
  }
  return null;
};

const DynamicAnalytics = ({ chartData, metrics }) => {
  const gaugeData = [
    { name: "Risk", value: metrics.infection_risk_pct, fill: "#f59e0b" },
    { name: "Safe", value: 100 - metrics.infection_risk_pct, fill: "#f1f5f9" },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      <Card className="lg:col-span-2">
        <CardHeader>
          <CardTitle className="text-sm font-medium">
            Healing Score Trend
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-48 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart
                data={chartData}
                margin={{ top: 5, right: 0, left: -20, bottom: 0 }}
              >
                <defs>
                  <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid
                  strokeDasharray="3 3"
                  vertical={false}
                  stroke="#e2e8f0"
                />
                <XAxis
                  dataKey="day"
                  axisLine={false}
                  tickLine={false}
                  tick={{ fontSize: 12, fill: "#64748b" }}
                  tickFormatter={(val) => `D${val}`}
                />
                <YAxis
                  axisLine={false}
                  tickLine={false}
                  tick={{ fontSize: 12, fill: "#64748b" }}
                  domain={[0, 100]}
                />
                <RechartsTooltip content={<CustomTooltip />} />
                <Area
                  type="monotone"
                  dataKey="score"
                  stroke="#10b981"
                  strokeWidth={3}
                  fillOpacity={1}
                  fill="url(#colorScore)"
                  name="Score"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-sm font-medium">
            Wound Area (mm²)
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-48 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={chartData}
                margin={{ top: 5, right: 0, left: -20, bottom: 0 }}
              >
                <CartesianGrid
                  strokeDasharray="3 3"
                  vertical={false}
                  stroke="#e2e8f0"
                />
                <XAxis
                  dataKey="day"
                  axisLine={false}
                  tickLine={false}
                  tick={{ fontSize: 12, fill: "#64748b" }}
                  tickFormatter={(val) => `D${val}`}
                />
                <YAxis
                  axisLine={false}
                  tickLine={false}
                  tick={{ fontSize: 12, fill: "#64748b" }}
                />
                <RechartsTooltip
                  content={<CustomTooltip />}
                  cursor={{ fill: "#f1f5f9" }}
                />
                <Bar dataKey="area" radius={[4, 4, 0, 0]} name="Area">
                  {chartData.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={
                        index === chartData.length - 1 &&
                        entry.area > chartData[index - 1]?.area
                          ? "#f43f5e"
                          : "#cbd5e1"
                      }
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-sm font-medium">
            Infection Risk Model
          </CardTitle>
        </CardHeader>
        <CardContent className="flex flex-col items-center justify-center relative">
          <div className="h-40 w-full relative">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={gaugeData}
                  cx="50%"
                  cy="100%"
                  startAngle={180}
                  endAngle={0}
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={0}
                  dataKey="value"
                  stroke="none"
                >
                  {gaugeData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
            <div className="absolute bottom-0 left-0 right-0 text-center pb-2">
              <span className="text-3xl font-bold text-slate-900">
                {metrics.infection_risk_pct}%
              </span>
              <p className="text-xs text-slate-500 font-medium uppercase tracking-wider">
                {metrics.risk_level}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

const AIReports = ({ aiReport }) => {
  const [activeTab, setActiveTab] = useState("doctor");

  return (
    <Card className="mb-6">
      <div className="border-b border-slate-200">
        <div className="flex px-4 pt-2 space-x-4">
          <button
            onClick={() => setActiveTab("doctor")}
            className={`flex items-center gap-2 pb-3 px-2 text-sm font-medium border-b-2 transition-colors ${
              activeTab === "doctor"
                ? "border-slate-900 text-slate-900"
                : "border-transparent text-slate-500 hover:text-slate-700"
            }`}
          >
            <FileText className="w-4 h-4" /> Doctor Summary
          </button>
          <button
            onClick={() => setActiveTab("patient")}
            className={`flex items-center gap-2 pb-3 px-2 text-sm font-medium border-b-2 transition-colors ${
              activeTab === "patient"
                ? "border-slate-900 text-slate-900"
                : "border-transparent text-slate-500 hover:text-slate-700"
            }`}
          >
            <CheckCircle2 className="w-4 h-4" /> Patient Care Advice
          </button>
        </div>
      </div>

      <CardContent className="pt-6 min-h-35">
        <AnimatePresence mode="wait">
          {activeTab === "doctor" && (
            <motion.div
              key="doctor"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2 }}
            >
              <div className="bg-slate-50 p-4 rounded-lg border border-slate-100 text-slate-700 leading-relaxed text-sm">
                <span className="font-semibold text-slate-900">
                  Clinical Note:{" "}
                </span>
                {aiReport.doctor_summary}
              </div>
            </motion.div>
          )}

          {activeTab === "patient" && (
            <motion.div
              key="patient"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2 }}
            >
              <ul className="space-y-3">
                {aiReport.patient_advice.map((advice, index) => (
                  <li
                    key={index}
                    className="flex items-start gap-3 text-sm text-slate-700"
                  >
                    <div className="mt-0.5 bg-emerald-100 rounded-full p-0.5 shrink-0">
                      <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                    </div>
                    <span>{advice}</span>
                  </li>
                ))}
              </ul>
            </motion.div>
          )}
        </AnimatePresence>
      </CardContent>
    </Card>
  );
};

// --- MODALS ---

const UploadModal = ({ isOpen, onClose, onUpload, isLoading, error }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [file, setFile] = useState(null);
  const [patientId, setPatientId] = useState("patient_001");
  const [day, setDay] = useState("3");

  if (!isOpen) return null;

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  const handleUploadClick = async () => {
    if (!file) return;
    await onUpload(file, patientId, day);
    // Reset form after upload
    setFile(null);
    setPatientId("patient_001");
    setDay("3");
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center px-4 bg-slate-900/50 backdrop-blur-sm"
      onClick={() => !isLoading && onClose()}
    >
      <motion.div
        initial={{ opacity: 0, scale: 0.95, y: 10 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.95, y: 10 }}
        onClick={(e) => e.stopPropagation()}
        className="bg-white rounded-xl shadow-xl w-full max-w-md overflow-hidden flex flex-col max-h-[90vh]"
      >
        <div className="flex justify-between items-center p-6 border-b border-slate-100">
          <h2 className="text-lg font-semibold">Upload New Scan</h2>
          <button
            onClick={onClose}
            disabled={isLoading}
            className="text-slate-400 hover:text-slate-600 transition-colors p-1 rounded-md hover:bg-slate-100 disabled:opacity-50"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-6 space-y-4 overflow-y-auto flex-1">
          {error && (
            <div className="p-3 bg-red-50 border border-red-200 rounded-lg flex gap-2 text-sm text-red-700">
              <AlertIcon className="w-4 h-4 shrink-0 mt-0.5" />
              <span>{error}</span>
            </div>
          )}

          <div
            className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors cursor-pointer group relative ${
              isDragging
                ? "border-emerald-500 bg-emerald-50"
                : "border-slate-200 hover:bg-slate-50"
            } ${isLoading ? "opacity-50 cursor-not-allowed" : ""}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() =>
              !isLoading && document.getElementById("file-upload").click()
            }
          >
            <input
              type="file"
              id="file-upload"
              className="hidden"
              accept="image/png, image/jpeg"
              onChange={(e) => setFile(e.target.files[0])}
              disabled={isLoading}
            />

            <div
              className={`w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3 transition-colors ${
                isDragging
                  ? "bg-emerald-100"
                  : "bg-slate-100 group-hover:bg-slate-200"
              }`}
            >
              {file ? (
                <ImageIcon className="w-6 h-6 text-emerald-600" />
              ) : (
                <UploadCloud
                  className={`w-6 h-6 ${isDragging ? "text-emerald-600" : "text-slate-500"}`}
                />
              )}
            </div>
            <p className="text-sm font-medium text-slate-900">
              {file
                ? file.name
                : isDragging
                  ? "Drop file here"
                  : "Click to upload or drag and drop"}
            </p>
            <p className="text-xs text-slate-500 mt-1">
              {file ? "File ready to process" : "PNG or JPG (max. 10MB)"}
            </p>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <label
                htmlFor="patient-id"
                className="text-sm font-medium text-slate-700"
              >
                Patient ID
              </label>
              <input
                id="patient-id"
                type="text"
                value={patientId}
                onChange={(e) => setPatientId(e.target.value)}
                disabled={isLoading}
                className="w-full px-3 py-2 text-sm border border-slate-200 rounded-md focus:outline-none focus:ring-2 focus:ring-slate-900 focus:border-transparent disabled:opacity-50"
                placeholder="e.g., patient_001"
              />
            </div>
            <div className="space-y-2">
              <label
                htmlFor="day"
                className="text-sm font-medium text-slate-700"
              >
                Monitoring Day
              </label>
              <input
                id="day"
                type="number"
                min="1"
                value={day}
                onChange={(e) => setDay(e.target.value)}
                disabled={isLoading}
                className="w-full px-3 py-2 text-sm border border-slate-200 rounded-md focus:outline-none focus:ring-2 focus:ring-slate-900 focus:border-transparent disabled:opacity-50"
                placeholder="e.g., 3"
              />
            </div>
          </div>
        </div>

        <div className="p-4 bg-slate-50 border-t border-slate-100 flex justify-end gap-2 shrink-0">
          <Button variant="ghost" onClick={onClose} disabled={isLoading}>
            Cancel
          </Button>
          <Button
            onClick={handleUploadClick}
            disabled={!file || isLoading}
            className="flex items-center gap-2"
          >
            {isLoading && <Loader className="w-4 h-4 animate-spin" />}
            {isLoading ? "Processing..." : "Analyze Scan"}
          </Button>
        </div>
      </motion.div>
    </div>
  );
};

// --- MAIN APP COMPONENT ---

export default function App() {
  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
  const [patientData, setPatientData] = useState(DEFAULT_DATA);
  const [isLoading, setIsLoading] = useState(false);
  const [uploadError, setUploadError] = useState(null);

  const handleUploadImage = async (file, patientId, day) => {
    setIsLoading(true);
    setUploadError(null);

    try {
      const formData = new FormData();
      formData.append("image", file);
      formData.append("patient_id", patientId);
      formData.append("day", day);

      const response = await fetch(`${API_BASE_URL}/api/upload`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Upload failed");
      }

      const result = await response.json();

      if (result.success) {
        // Update patient data with results from backend
        setPatientData({
          patient_id: result.patient_id,
          current_day: result.day,
          metrics: result.metrics,
          chartData: [
            { day: 1, score: 50, redness: 0.8, area: 1000 },
            { day: 2, score: 62, redness: 0.6, area: 1050 },
            {
              day: result.day,
              score: result.metrics.healing_score,
              redness: result.metrics.redness,
              area: result.metrics.wound_area,
            },
          ],
          ai_report: result.report,
        });

        setIsUploadModalOpen(false);
      } else {
        throw new Error("Invalid response format");
      }
    } catch (error) {
      console.error("Upload error:", error);
      setUploadError(
        error.message ||
          "Failed to process image. Make sure the backend server is running on http://localhost:5000",
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 p-4 md:p-8 font-sans selection:bg-emerald-200 selection:text-emerald-900">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <Header
            onUploadClick={() => setIsUploadModalOpen(true)}
            patientData={patientData}
          />
          <MetricsBanner metrics={patientData.metrics} />
          <VisualAnalysis />
          <DynamicAnalytics
            chartData={patientData.chartData}
            metrics={patientData.metrics}
          />
          <AIReports aiReport={patientData.ai_report} />
        </motion.div>
      </div>

      <AnimatePresence>
        {isUploadModalOpen && (
          <UploadModal
            isOpen={isUploadModalOpen}
            onClose={() => setIsUploadModalOpen(false)}
            onUpload={handleUploadImage}
            isLoading={isLoading}
            error={uploadError}
          />
        )}
      </AnimatePresence>
    </div>
  );
}
