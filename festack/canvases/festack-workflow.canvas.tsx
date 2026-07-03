import {
  Stack,
  Row,
  Grid,
  H1,
  H2,
  H3,
  Text,
  Code,
  Pill,
  Table,
  Callout,
  Card,
  CardHeader,
  CardBody,
  Divider,
  Stat,
  Link,
} from "cursor/canvas";

const ROOT = "skills";
const AGENTS = "agents";

function Cmd({ name, file }: { name: string; file: string }) {
  return (
    <Link href={`${ROOT}/${file}`}>
      <Code>{name}</Code>
    </Link>
  );
}

function Agent({ name }: { name: string }) {
  return (
    <Link href={`${AGENTS}/${name}.md`}>
      <Code>{name}</Code>
    </Link>
  );
}

function Ref({ label, file }: { label: string; file: string }) {
  return (
    <Link href={`${ROOT}/${file}`}>
      <Text as="span" size="small" tone="tertiary">
        {label}
      </Text>
    </Link>
  );
}

function FlowStep({
  label,
  detail,
  active,
}: {
  label: string;
  detail?: string;
  active?: boolean;
}) {
  return (
    <Stack gap={6} style={{ flex: "0 0 auto", width: "auto", maxWidth: 240 }}>
      <Pill active={active}>{label}</Pill>
      {detail ? (
        <Text size="small" tone="secondary" style={{ lineHeight: 1.4 }}>
          {detail}
        </Text>
      ) : null}
    </Stack>
  );
}

function FlowArrow() {
  return (
    <Text
      as="span"
      tone="tertiary"
      style={{
        flex: "0 0 auto",
        alignSelf: "center",
        padding: "0 4px",
        lineHeight: 1,
      }}
    >
      {"\u2192"}
    </Text>
  );
}

function FlowRow({ steps }: { steps: { label: string; detail?: string }[] }) {
  return (
    <Row gap={12} align="flex-start" wrap style={{ rowGap: 16 }}>
      {steps.flatMap((step, i) => {
        const nodes = [
          <FlowStep
            key={`step-${i}`}
            label={step.label}
            detail={step.detail}
            active={i === 0}
          />,
        ];
        if (i < steps.length - 1) {
          nodes.push(<FlowArrow key={`arrow-${i}`} />);
        }
        return nodes;
      })}
    </Row>
  );
}

export default function FestackWorkflow() {
  return (
    <Stack gap={24} style={{ padding: 24, maxWidth: 980 }}>
      <Stack gap={8}>
        <H1>/festack workflow cheat sheet</H1>
        <Text tone="secondary">
          Start at <Code>/festack</Code> when you have a situation, not a skill
          name. Narrow deliverables route to one skill. Broad outcomes hand off
          to <Agent name="festack-delivery-agent" />, which picks a playbook,
          resolves capabilities, and sequences the work. Design before build;
          <Code>/autopilot</Code> only after explicit approval.
        </Text>
        <Row gap={8} wrap>
          <Pill active>21 skills</Pill>
          <Pill>2 agents</Pill>
          <Pill>8 playbooks</Pill>
          <Pill>vendor-neutral core</Pill>
        </Row>
      </Stack>

      <Grid columns={3} gap={16}>
        <Stat value="/festack" label="canonical front door" />
        <Stat value="1" label="setup command: /setup-festack" />
        <Stat value="8" label="approved-build payload fields" />
      </Grid>

      <Callout tone="info" title="Three-second routing rule">
        <Stack gap={6}>
          <Text>
            Match on <Text as="span" weight="semibold">intent</Text>, not
            keywords. One clear narrow skill? Route directly. Outcome spans
            phases? Use the delivery agent. Genuinely torn between deliverables?
            Ask once with <Code>AskQuestion</Code>, then move.
          </Text>
          <Text tone="secondary">
            Missing profile or model config → <Cmd name="/setup-festack" file="setup-festack/SKILL.md" />.
            Missing capability registry → default-only mode is fine unless a
            required company provider is needed.
          </Text>
        </Stack>
      </Callout>

      <Stack gap={12}>
        <H2>Core workflow</H2>
        <Text tone="secondary">
          Source:{" "}
          <Ref
            label="routing-table.md"
            file="festack/references/routing-table.md"
          />
          ,{" "}
          <Ref label="playbooks.md" file="festack/references/playbooks.md" />
        </Text>
        <Card>
          <CardHeader>Narrow path — you know the deliverable</CardHeader>
          <CardBody>
            <FlowRow
              steps={[
                { label: "User ask" },
                { label: "/festack", detail: "classify intent" },
                { label: "One skill", detail: "hand off" },
                { label: "/review-work", detail: "if client-facing" },
              ]}
            />
          </CardBody>
        </Card>
        <Card>
          <CardHeader>Broad path — lazy end-to-end FE work</CardHeader>
          <CardBody>
            <FlowRow
              steps={[
                { label: "User outcome" },
                { label: "/festack" },
                { label: "festack-delivery-agent", detail: "choose playbook" },
                { label: "Capability registry", detail: "core or company" },
                { label: "Skills + gates" },
                { label: "/autopilot", detail: "approved only" },
              ]}
            />
          </CardBody>
        </Card>
        <Card>
          <CardHeader>Build path — design first, always</CardHeader>
          <CardBody>
            <FlowRow
              steps={[
                { label: "/demo | /poc | /solution-critic" },
                { label: "Explicit approval" },
                { label: "Approved-build payload" },
                { label: "/autopilot" },
              ]}
            />
          </CardBody>
        </Card>
      </Stack>

      <Stack gap={12}>
        <H2>Tie-breakers — confusable clusters</H2>
        <Table
          headers={["If the fork is...", "Route to", "Example ask"]}
          columnAlign={["left", "left", "left"]}
          rows={[
            [
              "Nothing agreed yet; define success and scope",
              <Cmd name="/scope-and-align" file="scope-and-align/SKILL.md" />,
              "Help me frame this engagement",
            ],
            [
              "Problem is fuzzy; understand before designing",
              <Cmd name="/problem-frame" file="problem-frame/SKILL.md" />,
              "Frame their batch-latency problem",
            ],
            [
              "Competing approaches; pick one with rationale",
              <Cmd name="/solution-critic" file="solution-critic/SKILL.md" />,
              "Approach A or B for their pipeline?",
            ],
            [
              "Whole account picture before engaging",
              <Cmd name="/discovery" file="discovery/SKILL.md" />,
              "Research this client before our first call",
            ],
            [
              "One specific product/support question",
              <Cmd name="/client-debug" file="client-debug/SKILL.md" />,
              "Does feature X support Y?",
            ],
            [
              "Product answer + client-ready packaging",
              <Agent name="festack-delivery-agent" />,
              "Answer for the client email with citations",
            ],
            [
              "Architecture already decided; just draw it",
              <Cmd name="/diagram" file="diagram/SKILL.md" />,
              "Draw the target architecture",
            ],
            [
              "Design architecture then draw or document",
              <Agent name="festack-delivery-agent" />,
              "Design the stack and put it in a doc",
            ],
            [
              "Quick fair comparison",
              <Cmd name="/compete" file="compete/SKILL.md" />,
              "Why us over Snowflake?",
            ],
            [
              "Battlecard, proof asset, competitive demo",
              <Agent name="festack-delivery-agent" />,
              "Make a battlecard with cited claims",
            ],
          ]}
        />
      </Stack>

      <Stack gap={12}>
        <H2>Playbooks — when the delivery agent takes over</H2>
        <Table
          headers={["Playbook", "Use when", "Key steps"]}
          columnAlign={["left", "left", "left"]}
          rows={[
            [
              <Code>account-prep</Code>,
              "Prep for account, call, or transition",
              "research.account → optional usage/risks → align → doc → review",
            ],
            [
              <Code>product-question-to-client-answer</Code>,
              "Customer product/support question",
              "research.product_question → optional client doc → review",
            ],
            [
              <Code>architecture-decision-to-diagram</Code>,
              "Design + visualize architecture",
              "frame.problem? → decide.approach → create.diagram → review",
            ],
            [
              <Code>competitive-proof-asset</Code>,
              "Battlecard, proof, competitive demo",
              "align → research.competitor → demo/doc → review → build?",
            ],
            [
              <Code>demo-design</Code>,
              "Scope or design a customer demo",
              "align? → design.demo → review → build?",
            ],
            [
              <Code>poc-scope</Code>,
              "POC / pilot / evaluation contract",
              "align? → scope.poc → review → build?",
            ],
            [
              <Code>doc-from-existing-artifact</Code>,
              "Package existing notes/diagram into doc",
              "create.client_doc → fe-deslop? → review",
            ],
            [
              <Code>approved-build</Code>,
              "Approved plan ready to execute",
              "build.approved_scope → review if client-facing",
            ],
          ]}
        />
      </Stack>

      <Stack gap={12}>
        <H2>Visual artifacts — who renders what</H2>
        <Text tone="secondary">
          Use canvas when structure helps the FE and customer team reason
          together. The deliverable owner renders; composed skills return
          structured handoffs so one flow does not stack redundant canvases.
        </Text>
        <Table
          headers={["Surface", "Owner", "Use when"]}
          columnAlign={["left", "left", "left"]}
          rows={[
            ["Canvas", "/scope-and-align, /discovery, /problem-frame, /solution-critic, /poc, /diagram, direct /review-work", "Briefs, account pictures, problem maps, decisions, POC criteria, diagrams, ranked findings"],
            ["Canvas + docs-canvas", "/demo", "Demo spine and shared picture, plus full blueprint and run of show"],
            ["Docs-canvas", "/doc or /demo", "Long docs, runbooks, large FAQs, or demo run-of-show navigation"],
            ["Structured handoff", "Composed /review-work, /client-debug, /diagram", "Caller owns the final artifact and consumes findings, citations, exports, or captions"],
            ["Plain prose", "/client-debug fast, /compete fast, trivial frames", "Short answers where a visual surface would add friction"],
          ]}
        />
        <Callout tone="info" title="Multi-agent quality bar">
          <Text>
            <Code>/solution-critic</Code>, <Code>/review-work</Code>, and
            <Code>festack-debate</Code> run panels where judgment compounds. If
            nested fan-out is blocked, return a parent-action gate instead of
            silently degrading to one model.
          </Text>
        </Callout>
      </Stack>

      <Stack gap={12}>
        <H2>Command palette — quick pick</H2>
        <Grid columns={2} gap={16}>
          <Stack gap={10}>
            <H3>Setup</H3>
            <Table
              headers={["Command", "Role"]}
              rows={[
                [<Cmd name="/festack" file="festack/SKILL.md" />, "Front door and router"],
                [<Cmd name="/setup-festack" file="setup-festack/SKILL.md" />, "One guided setup flow"],
                [<Cmd name="/personalize" file="personalize/SKILL.md" />, "Profile and voice"],
                [<Cmd name="/setup-models" file="setup-models/SKILL.md" />, "Model roles"],
                [<Cmd name="/setup-capabilities" file="setup-capabilities/SKILL.md" />, "Provider wiring"],
              ]}
            />
          </Stack>
          <Stack gap={10}>
            <H3>Reasoning primitives</H3>
            <Table
              headers={["Command", "Role"]}
              rows={[
                [<Cmd name="/problem-frame" file="problem-frame/SKILL.md" />, "Structure fuzzy problem"],
                [<Cmd name="/solution-critic" file="solution-critic/SKILL.md" />, "Debate approaches"],
                [<Cmd name="/review-work" file="review-work/SKILL.md" />, "Red-team deliverable"],
                [<Cmd name="/fe-deslop" file="fe-deslop/SKILL.md" />, "Clean AI prose"],
                [<Code>festack-debate</Code>, "Internal panel engine (composed, not typed)"],
              ]}
            />
          </Stack>
        </Grid>
        <Table
          headers={["Engagement command", "Role"]}
          columnAlign={["left", "left"]}
          rows={[
            [<Cmd name="/scope-and-align" file="scope-and-align/SKILL.md" />, "Align goal, audience, success criteria"],
            [<Cmd name="/discovery" file="discovery/SKILL.md" />, "Account research with citations"],
            [<Cmd name="/demo" file="demo/SKILL.md" />, "Design demo before build"],
            [<Cmd name="/diagram" file="diagram/SKILL.md" />, "Client-ready diagram"],
            [<Cmd name="/doc" file="doc/SKILL.md" />, "Client-ready document"],
            [<Cmd name="/poc" file="poc/SKILL.md" />, "POC contract with measurable exit"],
            [<Cmd name="/compete" file="compete/SKILL.md" />, "Fair competitive research"],
            [<Cmd name="/client-debug" file="client-debug/SKILL.md" />, "Cited product answer"],
            [<Cmd name="/autopilot" file="autopilot/SKILL.md" />, "Execute approved scope"],
            [<Cmd name="/retro" file="retro/SKILL.md" />, "Engagement reflection"],
            [<Cmd name="/learn" file="learn/SKILL.md" />, "Profile + lessons updates"],
          ]}
        />
      </Stack>

      <Stack gap={12}>
        <H2>Example journeys</H2>
        <Grid columns={1} gap={12}>
          <Card>
            <CardHeader>Account call prep</CardHeader>
            <CardBody>
              <FlowRow
                steps={[
                  { label: "/festack" },
                  { label: "account-prep" },
                  { label: "/discovery" },
                  { label: "/doc" },
                  { label: "/review-work" },
                ]}
              />
            </CardBody>
          </Card>
          <Card>
            <CardHeader>Client product question</CardHeader>
            <CardBody>
              <FlowRow
                steps={[
                  { label: "/festack" },
                  { label: "product-question playbook" },
                  { label: "/client-debug" },
                  { label: "/doc" },
                  { label: "/review-work" },
                ]}
              />
            </CardBody>
          </Card>
          <Card>
            <CardHeader>Demo then build</CardHeader>
            <CardBody>
              <FlowRow
                steps={[
                  { label: "Spine" },
                  { label: "/solution-critic" },
                  { label: "Blueprint" },
                  { label: "/review-work" },
                  { label: "Canvas + docs-canvas" },
                  { label: "approval gate" },
                  { label: "/autopilot" },
                ]}
              />
            </CardBody>
          </Card>
          <Card>
            <CardHeader>POC scope</CardHeader>
            <CardBody>
              <FlowRow
                steps={[
                  { label: "/festack" },
                  { label: "poc-scope" },
                  { label: "/poc" },
                  { label: "/review-work" },
                  { label: "approval gate" },
                  { label: "/autopilot?" },
                ]}
              />
            </CardBody>
          </Card>
          <Card>
            <CardHeader>Competitive proof asset</CardHeader>
            <CardBody>
              <FlowRow
                steps={[
                  { label: "/festack" },
                  { label: "competitive-proof-asset" },
                  { label: "/compete" },
                  { label: "/demo or /doc" },
                  { label: "/review-work" },
                  { label: "/autopilot?" },
                ]}
              />
            </CardBody>
          </Card>
          <Card>
            <CardHeader>Architecture decision to diagram</CardHeader>
            <CardBody>
              <FlowRow
                steps={[
                  { label: "/festack" },
                  { label: "/problem-frame?" },
                  { label: "/solution-critic" },
                  { label: "/diagram" },
                  { label: "/review-work" },
                ]}
              />
            </CardBody>
          </Card>
        </Grid>
      </Stack>

      <Stack gap={12}>
        <H2>Setup and config</H2>
        <Table
          headers={["What", "Where", "Written by"]}
          columnAlign={["left", "left", "left"]}
          rows={[
            ["Profile", "$FESTACK_HOME/profile.md", "/personalize"],
            ["Model roles", "host model-role config (Cursor: festack-models.mdc)", "/setup-models"],
            ["Capabilities", "$FESTACK_HOME/capabilities.md or .yaml", "/setup-capabilities"],
            ["Lessons", "$FESTACK_HOME/lessons.md", "/learn"],
            ["Starter registries", "samples/capabilities-*.yaml in repo", "copy + adjust providers"],
          ]}
        />
        <Callout tone="warning" title="/autopilot build gate">
          <Text>
            Do not route to <Code>/autopilot</Code> without an approved artifact
            or equivalent payload: approved scope, asset/phase list, acceptance
            checks, target environment, build adapter, deploy/export target,
            review status, and rollback/failure evidence for deployed work.
          </Text>
        </Callout>
      </Stack>

      <Stack gap={10}>
        <H2>Agents</H2>
        <Table
          headers={["Agent", "When to use"]}
          rows={[
            [
              <Agent name="festack-delivery-agent" />,
              "Broad FE outcomes, multi-phase playbooks, packaging after research",
            ],
            [
              <Agent name="festack-agent" />,
              "Stateless worker for debate panels, review, research, evaluator jobs",
            ],
          ]}
        />
      </Stack>

      <Divider />
      <Text tone="tertiary" size="small">
        festack workflow reference · skills at {ROOT} · agents at {AGENTS} ·
        canonical router: festack/references/routing-table.md
      </Text>
    </Stack>
  );
}
