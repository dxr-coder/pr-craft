import { useState, useEffect } from "react";
import {
  Button, Input, Table, Tag, Card, Typography, Space, message,
  Drawer, Spin, Popconfirm, Statistic, Row, Col, Empty, Flex,
} from "antd";
import {
  PlusOutlined, ReloadOutlined, GithubOutlined,
  FileTextOutlined, DeleteOutlined, CodeOutlined,
} from "@ant-design/icons";

const { Title, Paragraph, Text } = Typography;
const { TextArea } = Input;
const API_BASE = "http://localhost:8000";

const statusColors = { pending: "default", processing: "processing", done: "success", failed: "error" };
const statusLabels = { pending: "等待中", processing: "处理中", done: "已完成", failed: "失败" };

function App() {
  const [tasks, setTasks] = useState([]);
  const [issue, setIssue] = useState("");
  const [creating, setCreating] = useState(false);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [selectedTask, setSelectedTask] = useState(null);
  const [detailLoading, setDetailLoading] = useState(false);
  const [deleting, setDeleting] = useState(null);

  const fetchTasks = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/tasks/`);
      setTasks(await res.json());
    } catch { /* ignore */ }
  };

  useEffect(() => { fetchTasks(); }, []);

  useEffect(() => {
    const hasProcessing = tasks.some((t) => t.status === "pending" || t.status === "processing");
    if (!hasProcessing) return;
    const timer = setInterval(fetchTasks, 3000);
    return () => clearInterval(timer);
  }, [tasks]);

  const createTask = async () => {
    if (!issue.trim()) { message.warning("请输入需求描述"); return; }
    setCreating(true);
    try {
      await fetch(`${API_BASE}/api/tasks/?issue=${encodeURIComponent(issue)}`, { method: "POST" });
      message.success("任务已创建，正在后台运行");
      setIssue("");
      fetchTasks();
    } catch { message.error("创建失败"); }
    finally { setCreating(false); }
  };

  const deleteTask = async (id) => {
    setDeleting(id);
    try {
      await fetch(`${API_BASE}/api/tasks/${id}`, { method: "DELETE" });
      message.success("任务已删除");
      if (selectedTask?.id === id) { setDrawerOpen(false); setSelectedTask(null); }
      fetchTasks();
    } catch { message.error("删除失败"); }
    finally { setDeleting(null); }
  };

  const openDetail = async (id) => {
    setDrawerOpen(true);
    setDetailLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/tasks/${id}`);
      setSelectedTask(await res.json());
    } catch { message.error("获取详情失败"); }
    finally { setDetailLoading(false); }
  };

  const stats = {
    total: tasks.length,
    done: tasks.filter((t) => t.status === "done").length,
    failed: tasks.filter((t) => t.status === "failed").length,
    processing: tasks.filter((t) => t.status === "processing").length,
  };

  const columns = [
    { title: "#", key: "index", width: 50, render: (_, __, i) => i + 1 },
    {
      title: "需求", dataIndex: "issue", key: "issue", ellipsis: true,
      render: (t) => <span style={{ wordBreak: "break-word" }}>{t}</span>,
    },
    {
      title: "状态", dataIndex: "status", key: "status", width: 90,
      render: (s) => <Tag color={statusColors[s]} style={{ margin: 0 }}>{statusLabels[s] || s}</Tag>,
    },
    {
      title: "PR", dataIndex: "pr_url", key: "pr_url", width: 130,
      render: (url) => url
        ? <a href={url} target="_blank" rel="noreferrer" onClick={(e) => e.stopPropagation()}><GithubOutlined /> PR</a>
        : <Text type="secondary">-</Text>,
    },
    {
      title: "操作", key: "action", width: 120,
      render: (_, record) => (
        <Flex gap={4}>
          <Button type="link" size="small" icon={<FileTextOutlined />} onClick={(e) => { e.stopPropagation(); openDetail(record.id); }}>
            详情
          </Button>
          <Popconfirm title="确定删除这个任务？" onConfirm={() => deleteTask(record.id)} okText="删除" cancelText="取消">
            <Button type="link" size="small" danger icon={<DeleteOutlined />} loading={deleting === record.id} onClick={(e) => e.stopPropagation()}>
              删除
            </Button>
          </Popconfirm>
        </Flex>
      ),
    },
  ];

  return (
    <div style={{ minHeight: "100vh", background: "#f0f2f5" }}>
      {/* Header */}
      <div style={{
        background: "linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%)",
        padding: "60px 24px 50px",
        color: "#fff",
        position: "relative",
        overflow: "hidden",
        boxShadow: "0 4px 30px rgba(0,0,0,0.3)",
      }}>
        {/* 背景装饰网格 */}
        <div style={{
          position: "absolute", inset: 0,
          backgroundImage: "linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px)",
          backgroundSize: "60px 60px",
          pointerEvents: "none",
        }} />
        {/* 背景光晕 */}
        <div style={{
          position: "absolute", top: "-50%", right: "-10%",
          width: 500, height: 500,
          background: "radial-gradient(circle, rgba(120, 80, 255, 0.15) 0%, transparent 70%)",
          borderRadius: "50%",
          pointerEvents: "none",
        }} />
        <div style={{
          position: "absolute", bottom: "-30%", left: "-5%",
          width: 400, height: 400,
          background: "radial-gradient(circle, rgba(0, 200, 255, 0.1) 0%, transparent 70%)",
          borderRadius: "50%",
          pointerEvents: "none",
        }} />
        <div style={{ maxWidth: 1200, margin: "0 auto", position: "relative", zIndex: 1 }}>
          <div style={{ display: "flex", alignItems: "baseline", gap: 16, marginBottom: 12 }}>
            <Title level={1} style={{
              color: "#fff", margin: 0, fontSize: 42,
              background: "linear-gradient(90deg, #fff, #a78bfa)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
              letterSpacing: "-1px",
            }}>
              PR Craft
            </Title>
            <Tag color="purple" style={{ fontSize: 13, padding: "2px 10px", borderRadius: 20 }}>v1.0</Tag>
          </div>
          <Paragraph style={{
            color: "rgba(255,255,255,0.6)", margin: 0, fontSize: 18,
            maxWidth: 600,
          }}>
            AI 自动化 PR 系统 · 输入需求，AI 自动完成代码编写、审查并提交 PR
          </Paragraph>
        </div>
      </div>

      <div style={{ maxWidth: 1200, margin: "0 auto", padding: "24px" }}>
        {/* 统计卡片 */}
        <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
          <Col xs={12} sm={6}><Card size="small"><Statistic title="总任务" value={stats.total} /></Card></Col>
          <Col xs={12} sm={6}><Card size="small"><Statistic title="已完成" value={stats.done} valueStyle={{ color: "#52c41a" }} /></Card></Col>
          <Col xs={12} sm={6}><Card size="small"><Statistic title="进行中" value={stats.processing} valueStyle={{ color: "#1677ff" }} /></Card></Col>
          <Col xs={12} sm={6}><Card size="small"><Statistic title="失败" value={stats.failed} valueStyle={{ color: "#ff4d4f" }} /></Card></Col>
        </Row>

        {/* 创建任务 */}
        <Card title="创建新任务" style={{ marginBottom: 24 }}>
          <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
            <TextArea
              rows={3}
              placeholder="输入需求描述，例如：写一个函数计算两个数的和"
              value={issue}
              onChange={(e) => setIssue(e.target.value)}
            />
            <Button type="primary" icon={<PlusOutlined />} onClick={createTask} loading={creating} size="large" style={{ alignSelf: "flex-start" }}>
              创建任务
            </Button>
          </div>
        </Card>

        {/* 任务列表 */}
        <Card
          title="任务列表"
          extra={<Button icon={<ReloadOutlined />} onClick={fetchTasks}>刷新</Button>}
        >
          <Table
            dataSource={tasks}
            columns={columns}
            rowKey="id"
            pagination={{ pageSize: 10, size: "small" }}
            size="small"
            locale={{ emptyText: <Empty description="暂无任务，输入需求创建一个吧" /> }}
            onRow={(record) => ({ onClick: () => openDetail(record.id), style: { cursor: "pointer" } })}
            scroll={{ x: 520 }}
          />
        </Card>
      </div>

      {/* 详情抽屉 */}
      <Drawer
        title={selectedTask ? `任务 #${selectedTask.id} 详情` : "任务详情"}
        placement="right"
        width={Math.min(680, window.innerWidth - 64)}
        open={drawerOpen}
        onClose={() => { setDrawerOpen(false); setSelectedTask(null); }}
        extra={
          selectedTask && (
            <Popconfirm title="确定删除？" onConfirm={() => deleteTask(selectedTask.id)} okText="删除" cancelText="取消">
              <Button danger icon={<DeleteOutlined />} loading={deleting === selectedTask.id}>删除</Button>
            </Popconfirm>
          )
        }
      >
        {detailLoading ? (
          <div style={{ textAlign: "center", padding: 80 }}><Spin size="large" /></div>
        ) : selectedTask ? (
          <div style={{ display: "flex", flexDirection: "column", gap: 20, overflow: "hidden" }}>
            {/* 状态 */}
            <div>
              <Text strong>状态：</Text>
              <Tag color={statusColors[selectedTask.status]}>{statusLabels[selectedTask.status]}</Tag>
            </div>

            {/* 需求描述 */}
            <div>
              <Text strong>需求描述</Text>
              <div style={{ background: "#fafafa", padding: 12, borderRadius: 6, marginTop: 4, wordBreak: "break-word" }}>
                {selectedTask.issue}
              </div>
            </div>

            {/* 方案 */}
            {selectedTask.plan && (
              <div>
                <Text strong>AI 方案</Text>
                <div style={{
                  background: "#fafafa", padding: 12, borderRadius: 6, marginTop: 4,
                  whiteSpace: "pre-wrap", wordBreak: "break-word", fontSize: 13, maxHeight: 300, overflow: "auto",
                }}>
                  {selectedTask.plan}
                </div>
              </div>
            )}

            {/* 代码 */}
            {selectedTask.code && (
              <div>
                <Text strong><CodeOutlined /> 生成代码</Text>
                <pre style={{
                  background: "#1e1e1e", color: "#d4d4d4", padding: 16,
                  borderRadius: 6, fontSize: 13, overflow: "auto", marginTop: 4,
                  maxHeight: 400, wordBreak: "break-all", whiteSpace: "pre-wrap",
                }}>
                  {selectedTask.code}
                </pre>
              </div>
            )}

            {/* 审查 */}
            {selectedTask.review && (
              <div>
                <Text strong>审查意见</Text>
                <div style={{ background: "#fafafa", padding: 12, borderRadius: 6, marginTop: 4, wordBreak: "break-word" }}>
                  {selectedTask.review}
                </div>
              </div>
            )}

            {/* PR 链接 */}
            {selectedTask.pr_url && (
              <Button type="primary" icon={<GithubOutlined />} href={selectedTask.pr_url} target="_blank" block>
                在 GitHub 上查看 PR
              </Button>
            )}
          </div>
        ) : null}
      </Drawer>
    </div>
  );
}

export default App;
