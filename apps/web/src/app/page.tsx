"use client";

import { useEffect, useState } from "react";

type IncidentRecord = {
  record_id: string;
  alert_id: string;
  service: string;
  analysis: {
    likely_cause: string;
    severity: string;
    recommended_action: string;
    confidence: string;
    requires_approval: boolean;
  };
  approval_status: string;
};

const SEVERITY_STYLES: Record<string, { border: string; text: string; dot: string }> = {
  critical: { border: "border-l-rose-500", text: "text-rose-400", dot: "bg-rose-500" },
  high: { border: "border-l-orange-500", text: "text-orange-400", dot: "bg-orange-500" },
  medium: { border: "border-l-amber-500", text: "text-amber-400", dot: "bg-amber-500" },
  low: { border: "border-l-sky-500", text: "text-sky-400", dot: "bg-sky-500" },
};

const STATUS_STYLES: Record<string, string> = {
  pending: "bg-amber-500/10 text-amber-400 border-amber-500/30",
  approved: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
  rejected: "bg-rose-500/10 text-rose-400 border-rose-500/30",
  not_required: "bg-gray-500/10 text-gray-400 border-gray-500/30",
};

export default function Home() {
  const [incidents, setIncidents] = useState<IncidentRecord[]>([]);
  const [loading, setLoading] = useState(true);

  const loadIncidents = () => {
    fetch("http://127.0.0.1:8000/incidents")
      .then((res) => res.json())
      .then((data) => {
        setIncidents(data);
        setLoading(false);
      });
  };

  useEffect(() => {
    loadIncidents();
  }, []);

  const handleApprove = async (recordId: string) => {
    const res = await fetch(`http://127.0.0.1:8000/incidents/${recordId}/approve`, {
      method: "POST",
    });
    const updated = await res.json();
    setIncidents((prev) => prev.map((i) => (i.record_id === recordId ? updated : i)));
  };

  const handleReject = async (recordId: string) => {
    const res = await fetch(`http://127.0.0.1:8000/incidents/${recordId}/reject`, {
      method: "POST",
    });
    const updated = await res.json();
    setIncidents((prev) => prev.map((i) => (i.record_id === recordId ? updated : i)));
  };

  const pendingCount = incidents.filter((i) => i.approval_status === "pending").length;

  return (
    <main className="min-h-screen">
      {/* Top bar */}
      <header className="border-b border-gray-800/80 bg-[#0D1117]/80 backdrop-blur sticky top-0 z-10">
        <div className="max-w-4xl mx-auto px-6 py-5 flex items-center justify-between">
          <div>
            <h1 className="font-[family-name:var(--font-mono)] text-xl font-bold tracking-tight text-white">
              OpsPilot
            </h1>
            <p className="text-sm text-gray-500 mt-0.5">
              Agentic SRE Incident Triage & Response Copilot
            </p>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <span className="text-gray-500">Live</span>
          </div>
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-6 py-8">
        {/* Stats row */}
        <div className="grid grid-cols-3 gap-4 mb-8">
          <div className="bg-[#0D1117] border border-gray-800/80 rounded-lg p-4">
            <p className="text-xs text-gray-500 uppercase tracking-wide font-[family-name:var(--font-mono)]">
              Total Incidents
            </p>
            <p className="text-2xl font-semibold text-white mt-1">{incidents.length}</p>
          </div>
          <div className="bg-[#0D1117] border border-gray-800/80 rounded-lg p-4">
            <p className="text-xs text-gray-500 uppercase tracking-wide font-[family-name:var(--font-mono)]">
              Pending Approval
            </p>
            <p className="text-2xl font-semibold text-amber-400 mt-1">{pendingCount}</p>
          </div>
          <div className="bg-[#0D1117] border border-gray-800/80 rounded-lg p-4">
            <p className="text-xs text-gray-500 uppercase tracking-wide font-[family-name:var(--font-mono)]">
              Resolved
            </p>
            <p className="text-2xl font-semibold text-emerald-400 mt-1">
              {incidents.length - pendingCount}
            </p>
          </div>
        </div>

        {/* Incident list */}
        {loading && (
          <p className="text-gray-500 font-[family-name:var(--font-mono)] text-sm">
            Loading incidents...
          </p>
        )}

        {!loading && incidents.length === 0 && (
          <div className="border border-dashed border-gray-800 rounded-lg p-10 text-center">
            <p className="text-gray-500">No incidents reported.</p>
            <p className="text-gray-600 text-sm mt-1">
              New alerts will appear here for triage.
            </p>
          </div>
        )}

        <div className="space-y-4">
          {incidents.map((incident) => {
            const sev = SEVERITY_STYLES[incident.analysis.severity] ?? SEVERITY_STYLES.low;
            const statusStyle = STATUS_STYLES[incident.approval_status] ?? STATUS_STYLES.not_required;

            return (
              <div
                key={incident.record_id}
                className={`bg-[#0D1117] border border-gray-800/80 border-l-4 ${sev.border} rounded-lg p-5`}
              >
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <div className="flex items-center gap-3">
                      <h2 className="font-[family-name:var(--font-mono)] font-semibold text-white">
                        {incident.alert_id}
                      </h2>
                      <span className="text-gray-600">·</span>
                      <span className="font-[family-name:var(--font-mono)] text-sm text-gray-400">
                        {incident.service}
                      </span>
                      <span className={`text-xs font-medium uppercase tracking-wide ${sev.text}`}>
                        {incident.analysis.severity}
                      </span>
                    </div>
                    <p className="text-gray-300 mt-2 text-sm leading-relaxed">
                      {incident.analysis.likely_cause}
                    </p>
                    <p className="text-gray-500 mt-2 text-sm">
                      <span className="text-gray-600">Recommended:</span>{" "}
                      {incident.analysis.recommended_action}
                    </p>
                  </div>

                  <span
                    className={`shrink-0 text-xs font-medium px-2.5 py-1 rounded-full border ${statusStyle} capitalize font-[family-name:var(--font-mono)]`}
                  >
                    {incident.approval_status.replace("_", " ")}
                  </span>
                </div>

                {incident.approval_status === "pending" && (
                  <div className="flex gap-2 mt-4 pt-4 border-t border-gray-800/60">
                    <button
                      onClick={() => handleApprove(incident.record_id)}
                      className="bg-emerald-600/90 hover:bg-emerald-500 text-white px-4 py-1.5 rounded-md text-sm font-medium transition-colors"
                    >
                      Approve
                    </button>
                    <button
                      onClick={() => handleReject(incident.record_id)}
                      className="bg-transparent hover:bg-rose-500/10 text-rose-400 border border-rose-500/30 px-4 py-1.5 rounded-md text-sm font-medium transition-colors"
                    >
                      Reject
                    </button>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </main>
  );
}