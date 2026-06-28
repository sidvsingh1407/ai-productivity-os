import React, { useState, useEffect } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { History, Eye, RefreshCw } from 'lucide-react';
import { projectsApi, PromptHistoryRecord } from '@/api/projects';
import { format } from 'date-fns';
import { Modal } from '@/components/ui/modal';

export function HistoryTab() {
  const [history, setHistory] = useState<PromptHistoryRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Modal state
  const [selectedRecord, setSelectedRecord] = useState<PromptHistoryRecord | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    setLoading(true);
    try {
      const data = await projectsApi.getPromptHistory();
      setHistory(data);
    } catch (err) {
      setError('Failed to load prompt history.');
    } finally {
      setLoading(false);
    }
  };

  const openModal = (record: PromptHistoryRecord) => {
    setSelectedRecord(record);
    setIsModalOpen(true);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-12">
        <RefreshCw className="w-8 h-8 text-blue-500 animate-spin" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-red-50 text-red-600 rounded-md">
        {error}
      </div>
    );
  }

  if (history.length === 0) {
    return (
      <div className="text-center p-12 border border-dashed rounded-lg border-slate-300 dark:border-slate-700">
        <History className="w-12 h-12 text-slate-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-slate-900 dark:text-slate-100">No history yet</h3>
        <p className="text-slate-500 dark:text-slate-400 mt-2">
          Prompts you improve will automatically appear here.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg overflow-hidden">
        <div className="grid grid-cols-12 gap-4 p-4 border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/50 text-xs font-medium text-slate-500 uppercase tracking-wider">
          <div className="col-span-8">Original Prompt</div>
          <div className="col-span-3">Date</div>
          <div className="col-span-1 text-right">Action</div>
        </div>

        <div className="divide-y divide-slate-100 dark:divide-slate-800">
          {history.map((record) => (
            <div key={record.id} className="grid grid-cols-12 gap-4 p-4 items-center hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">
              <div className="col-span-8">
                <p className="text-sm text-slate-900 dark:text-slate-100 truncate pr-4">
                  {record.original_prompt}
                </p>
              </div>
              <div className="col-span-3">
                <span className="text-xs text-slate-500 whitespace-nowrap">
                  {format(new Date(record.created_at), 'MMM d, yyyy h:mm a')}
                </span>
              </div>
              <div className="col-span-1 text-right">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => openModal(record)}
                  className="h-8 px-2 text-blue-600 hover:text-blue-700 hover:bg-blue-50"
                >
                  <Eye className="w-4 h-4 mr-1" />
                  View
                </Button>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="text-center py-4 text-xs text-slate-500">
        Showing last {history.length} prompts. Upgrade for full history.
      </div>

      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Prompt Details"
      >
        {selectedRecord && (
          <div className="space-y-6">
            <div>
              <h4 className="text-sm font-medium text-slate-900 dark:text-slate-100 mb-2">Original Prompt</h4>
              <div className="bg-slate-50 dark:bg-slate-900 p-4 rounded-md border border-slate-200 dark:border-slate-800 text-sm whitespace-pre-wrap max-h-48 overflow-y-auto">
                {selectedRecord.original_prompt}
              </div>
            </div>

            {selectedRecord.improved_prompt ? (
              <div>
                <h4 className="text-sm font-medium text-slate-900 dark:text-slate-100 mb-2">Improved Prompt</h4>
                <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-md border border-blue-100 dark:border-blue-800 text-sm whitespace-pre-wrap max-h-48 overflow-y-auto">
                  {selectedRecord.improved_prompt}
                </div>
              </div>
            ) : (
              <div className="text-sm text-slate-500 italic">
                No improved prompt available (validation may have failed).
              </div>
            )}

            <div className="text-xs text-slate-500 pt-2 border-t border-slate-100 dark:border-slate-800">
              Processed on {format(new Date(selectedRecord.created_at), 'MMMM d, yyyy h:mm a')}
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
}
