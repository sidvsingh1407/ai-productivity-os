import React, { useEffect, useState } from 'react';
import { aiSystemsApi, CapabilityMapResponse } from '../api/aiSystems';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { AlertCircle } from 'lucide-react';
import Layout from '../components/Layout';

const CapabilityMap: React.FC = () => {
  const [data, setData] = useState<CapabilityMapResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchMap = async () => {
      try {
        const result = await aiSystemsApi.getCapabilityMap();
        setData(result);
      } catch (err: any) {
        console.error('Error fetching capability map:', err);
        setError(err.message || 'Failed to load Capability Map');
      } finally {
        setLoading(false);
      }
    };
    fetchMap();
  }, []);

  const renderScore = (score: number | undefined, unavailableReason?: string) => {
    if (score !== undefined && score !== null) {
      return (
        <span className="text-lg font-semibold text-blue-600">
          {Math.round(score)} / 100
        </span>
      );
    }
    return (
      <span className="text-sm text-gray-500 italic flex items-center">
        <AlertCircle className="w-4 h-4 mr-1 text-gray-400" />
        {unavailableReason || 'Not available'}
      </span>
    );
  };

  return (

      <div className="p-8">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold text-gray-900">AI Capability Map</h1>
        </div>

        {error && (
          <div className="bg-red-50 text-red-700 p-4 rounded-md mb-6 flex items-center">
            <AlertCircle className="w-5 h-5 mr-2" />
            {error}
          </div>
        )}

        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1, 2, 3].map(i => (
              <Card key={i} className="h-64 flex flex-col justify-between p-4">
                 <div className="text-gray-500">Loading...</div>
              </Card>
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {data.map(sys => (
              <Card key={sys.id} className="hover:shadow-md transition-shadow">
                <CardHeader>
                  <CardTitle className="flex justify-between items-start">
                    <span className="truncate" title={sys.name}>{sys.name}</span>
                    {sys.lifecycle_status && (
                      <Badge variant="outline" className="ml-2 whitespace-nowrap">
                        {sys.lifecycle_status}
                      </Badge>
                    )}
                  </CardTitle>
                  <div className="text-sm text-gray-500 mt-1 flex flex-wrap gap-2">
                    {sys.ai_type && <span>Type: {sys.ai_type}</span>}
                    {sys.department && <span>• Dept: {sys.department}</span>}
                    {sys.owner && <span>• Owner: {sys.owner}</span>}
                  </div>
                </CardHeader>

                <CardContent>
                  <div className="space-y-4">
                    {/* Scores Section */}
                    <div className="grid grid-cols-2 gap-4 bg-gray-50 p-4 rounded-md">
                      <div>
                        <div className="text-xs text-gray-500 uppercase tracking-wider mb-1">Adoption Score</div>
                        {renderScore(sys.adoption_score, 'No adoption records')}
                      </div>
                      <div>
                        <div className="text-xs text-gray-500 uppercase tracking-wider mb-1">Data Score</div>
                        {renderScore(sys.data_score, 'No data fields populated')}
                      </div>
                      <div className="col-span-2 border-t border-gray-200 pt-3 mt-1">
                        <div className="text-xs text-gray-500 uppercase tracking-wider mb-1 flex justify-between">
                          <span>ROI Score</span>
                          {sys.cost_is_partial && (
                            <span className="text-amber-600 font-medium" title={`Missing: ${sys.cost_missing_components?.join(', ')}`}>
                              ⚠️ Partial Cost
                            </span>
                          )}
                        </div>
                        {renderScore(sys.roi_score, sys.roi_score_unavailable_reason)}
                      </div>
                    </div>

                    {/* Meta Section */}
                    {(sys.data_types?.length ? sys.data_types.length > 0 : false) && (
                      <div>
                        <div className="text-xs font-semibold text-gray-700 mb-2">Data Types</div>
                        <div className="flex flex-wrap gap-1">
                          {sys.data_types?.map(dt => (
                            <Badge key={dt} variant="secondary" className="text-xs">{dt}</Badge>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}

            {data.length === 0 && !error && (
              <div className="col-span-full text-center py-12 text-gray-500 bg-white rounded-lg border border-dashed border-gray-300">
                No AI systems found in the Capability Map. Add some in the Inventory first.
              </div>
            )}
          </div>
        )}
      </div>

  );
};

export default CapabilityMap;
