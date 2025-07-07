import React, { useState } from 'react';
import { Search, Users, Mail, Download, Play, CheckCircle, Clock, Sparkles, Bot, Target, FileText, ArrowRight, Globe, Building, MessageSquare } from 'lucide-react';

const LeadGenUI = () => {
  const [prompt, setPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [results, setResults] = useState(null);
  const [activeTab, setActiveTab] = useState('leads');
  const [showExample, setShowExample] = useState(false);

  const examplePrompts = [
    "Find manufacturing companies in Texas that could benefit from vision AI systems",
    "Research food processing companies in California that need quality control automation",
    "Find automotive suppliers in Michigan who might need industrial automation solutions",
    "Identify pharmaceutical companies in New Jersey that could use vision inspection systems"
  ];

  const mockResults = {
    leads: [
      {
        company: "Texas Instruments",
        website: "ti.com",
        description: "Leading semiconductor manufacturer with global operations",
        products: "Microcontrollers, processors, analog chips",
        match: "Vision AI for quality control in semiconductor fabrication processes"
      },
      {
        company: "Dell Technologies",
        website: "dell.com", 
        description: "Multinational computer technology company",
        products: "Laptops, servers, storage solutions",
        match: "Automation for assembly line optimization and component inspection"
      },
      {
        company: "Flex Ltd",
        website: "flex.com",
        description: "Electronics manufacturing services provider",
        products: "Consumer electronics, automotive components",
        match: "Vision systems for automated defect detection in electronics assembly"
      }
    ],
    emails: [
      {
        company: "Texas Instruments",
        subject: "Partnership Opportunity - Vision AI for Semiconductor Manufacturing",
        preview: "Dear Texas Instruments Team, I hope this email finds you well. I'm reaching out from Replicant Systems, a company specializing in AI-powered vision systems..."
      },
      {
        company: "Dell Technologies", 
        subject: "Industrial Automation Solutions for Manufacturing Excellence",
        preview: "Dear Dell Technologies Team, I noticed your commitment to manufacturing innovation and believe our industrial automation solutions could significantly enhance..."
      },
      {
        company: "Flex Ltd",
        subject: "Advanced Vision Systems for Electronics Manufacturing",
        preview: "Dear Flex Ltd Team, Your reputation for electronics manufacturing excellence caught our attention. At Replicant Systems, we specialize in vision AI..."
      }
    ]
  };

  const handleGenerate = async () => {
    if (!prompt.trim()) return;
    
    setIsGenerating(true);
    setResults(null);
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    setResults(mockResults);
    setIsGenerating(false);
  };

  const handleDownload = (type) => {
    const data = type === 'leads' ? results.leads : results.emails;
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${type}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-1/2 -right-1/2 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute -bottom-1/2 -left-1/2 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
      </div>

      <div className="relative z-10">
        {/* Header */}
        <header className="border-b border-white/10 backdrop-blur-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="bg-gradient-to-r from-purple-500 to-blue-500 p-2 rounded-xl">
                  <Bot className="w-8 h-8 text-white" />
                </div>
                <div>
                  <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
                    LeadGen AI
                  </h1>
                  <p className="text-gray-400 text-sm">Powered by Replicant Systems</p>
                </div>
              </div>
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2 text-sm text-gray-400">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                  <span>AI Agents Active</span>
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Hero Section */}
          <div className="text-center mb-12">
            <div className="flex items-center justify-center space-x-2 mb-4">
              <Sparkles className="w-6 h-6 text-purple-400" />
              <h2 className="text-4xl font-bold text-white">
                AI-Powered Lead Generation
              </h2>
              <Sparkles className="w-6 h-6 text-blue-400" />
            </div>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Automatically research companies, match them with your solutions, and generate personalized outreach emails using multi-agent AI orchestration.
            </p>
          </div>

          {/* Input Section */}
          <div className="bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10 p-8 mb-8">
            <div className="flex items-center space-x-3 mb-6">
              <Target className="w-6 h-6 text-purple-400" />
              <h3 className="text-xl font-semibold text-white">Define Your Target Market</h3>
            </div>
            
            <div className="relative mb-6">
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Describe your ideal leads (industry, location, specific needs)..."
                className="w-full h-32 bg-white/5 border border-white/20 rounded-xl px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
                disabled={isGenerating}
              />
              <div className="absolute bottom-3 right-3 flex space-x-2">
                <button
                  onClick={() => setShowExample(!showExample)}
                  className="p-2 text-gray-400 hover:text-white transition-colors"
                  title="Show examples"
                >
                  <FileText className="w-4 h-4" />
                </button>
              </div>
            </div>

            {showExample && (
              <div className="bg-white/5 rounded-lg p-4 mb-6 border border-white/10">
                <p className="text-sm text-gray-300 mb-3">Example prompts:</p>
                <div className="space-y-2">
                  {examplePrompts.map((example, index) => (
                    <button
                      key={index}
                      onClick={() => setPrompt(example)}
                      className="block w-full text-left p-2 rounded-lg hover:bg-white/10 transition-colors text-sm text-gray-300 hover:text-white"
                    >
                      "{example}"
                    </button>
                  ))}
                </div>
              </div>
            )}

            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4 text-sm text-gray-400">
                <div className="flex items-center space-x-1">
                  <Search className="w-4 h-4" />
                  <span>Research</span>
                </div>
                <ArrowRight className="w-4 h-4" />
                <div className="flex items-center space-x-1">
                  <Target className="w-4 h-4" />
                  <span>Match</span>
                </div>
                <ArrowRight className="w-4 h-4" />
                <div className="flex items-center space-x-1">
                  <Mail className="w-4 h-4" />
                  <span>Generate</span>
                </div>
              </div>
              
              <button
                onClick={handleGenerate}
                disabled={!prompt.trim() || isGenerating}
                className="flex items-center space-x-2 bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-600 hover:to-blue-600 disabled:opacity-50 disabled:cursor-not-allowed px-6 py-3 rounded-xl text-white font-medium transition-all duration-200 transform hover:scale-105"
              >
                {isGenerating ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
                    <span>Generating...</span>
                  </>
                ) : (
                  <>
                    <Play className="w-4 h-4" />
                    <span>Generate Leads</span>
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Progress Indicator */}
          {isGenerating && (
            <div className="bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10 p-6 mb-8">
              <div className="flex items-center justify-center space-x-4">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                  <span className="text-green-400">Researcher Agent</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-yellow-500 rounded-full animate-pulse delay-300"></div>
                  <span className="text-yellow-400">Matcher Agent</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-blue-500 rounded-full animate-pulse delay-700"></div>
                  <span className="text-blue-400">Email Agent</span>
                </div>
              </div>
            </div>
          )}

          {/* Results Section */}
          {results && (
            <div className="bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10 p-8">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center space-x-3">
                  <CheckCircle className="w-6 h-6 text-green-400" />
                  <h3 className="text-xl font-semibold text-white">Results Generated</h3>
                </div>
                <div className="flex items-center space-x-2 text-sm text-gray-400">
                  <Clock className="w-4 h-4" />
                  <span>Generated just now</span>
                </div>
              </div>

              {/* Tabs */}
              <div className="flex space-x-1 mb-6 bg-white/5 rounded-lg p-1">
                <button
                  onClick={() => setActiveTab('leads')}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all ${
                    activeTab === 'leads'
                      ? 'bg-purple-500 text-white shadow-lg'
                      : 'text-gray-400 hover:text-white hover:bg-white/10'
                  }`}
                >
                  <Users className="w-4 h-4" />
                  <span>Leads ({results.leads.length})</span>
                </button>
                <button
                  onClick={() => setActiveTab('emails')}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all ${
                    activeTab === 'emails'
                      ? 'bg-purple-500 text-white shadow-lg'
                      : 'text-gray-400 hover:text-white hover:bg-white/10'
                  }`}
                >
                  <Mail className="w-4 h-4" />
                  <span>Emails ({results.emails.length})</span>
                </button>
              </div>

              {/* Content */}
              {activeTab === 'leads' && (
                <div className="space-y-4">
                  <div className="flex justify-end">
                    <button
                      onClick={() => handleDownload('leads')}
                      className="flex items-center space-x-2 bg-white/10 hover:bg-white/20 px-4 py-2 rounded-lg text-white transition-colors"
                    >
                      <Download className="w-4 h-4" />
                      <span>Export Leads</span>
                    </button>
                  </div>
                  {results.leads.map((lead, index) => (
                    <div key={index} className="bg-white/5 rounded-lg p-6 border border-white/10 hover:border-purple-500/50 transition-colors">
                      <div className="flex items-start justify-between mb-4">
                        <div className="flex items-center space-x-3">
                          <div className="bg-gradient-to-r from-purple-500 to-blue-500 p-2 rounded-lg">
                            <Building className="w-5 h-5 text-white" />
                          </div>
                          <div>
                            <h4 className="text-lg font-semibold text-white">{lead.company}</h4>
                            <div className="flex items-center space-x-2 text-sm text-gray-400">
                              <Globe className="w-4 h-4" />
                              <span>{lead.website}</span>
                            </div>
                          </div>
                        </div>
                        <div className="bg-green-500/20 text-green-400 px-3 py-1 rounded-full text-sm">
                          High Match
                        </div>
                      </div>
                      <p className="text-gray-300 mb-4">{lead.description}</p>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                        <div>
                          <span className="text-gray-400">Products:</span>
                          <p className="text-white">{lead.products}</p>
                        </div>
                        <div>
                          <span className="text-gray-400">Match Opportunity:</span>
                          <p className="text-white">{lead.match}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {activeTab === 'emails' && (
                <div className="space-y-4">
                  <div className="flex justify-end">
                    <button
                      onClick={() => handleDownload('emails')}
                      className="flex items-center space-x-2 bg-white/10 hover:bg-white/20 px-4 py-2 rounded-lg text-white transition-colors"
                    >
                      <Download className="w-4 h-4" />
                      <span>Export Emails</span>
                    </button>
                  </div>
                  {results.emails.map((email, index) => (
                    <div key={index} className="bg-white/5 rounded-lg p-6 border border-white/10 hover:border-blue-500/50 transition-colors">
                      <div className="flex items-start justify-between mb-4">
                        <div className="flex items-center space-x-3">
                          <div className="bg-gradient-to-r from-blue-500 to-purple-500 p-2 rounded-lg">
                            <MessageSquare className="w-5 h-5 text-white" />
                          </div>
                          <div>
                            <h4 className="text-lg font-semibold text-white">{email.company}</h4>
                            <p className="text-sm text-gray-400">{email.subject}</p>
                          </div>
                        </div>
                        <button className="bg-blue-500/20 text-blue-400 px-3 py-1 rounded-full text-sm hover:bg-blue-500/30 transition-colors">
                          Copy Email
                        </button>
                      </div>
                      <div className="bg-white/5 rounded-lg p-4 border border-white/10">
                        <p className="text-gray-300 text-sm leading-relaxed">{email.preview}...</p>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </main>
      </div>
    </div>
  );
};

export default LeadGenUI;