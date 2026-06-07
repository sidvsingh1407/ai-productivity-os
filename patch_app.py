import re

with open('frontend/src/App.tsx', 'r') as f:
    content = f.read()

# Add the import
import_stmt = "import SettingsPage from './pages/Settings/SettingsPage';\n"
content = re.sub(r"(import PromptImprover from '\./pages/PromptImprover';\n)", r"\1" + import_stmt, content)

# Add the route
route_stmt = "          <Route path=\"settings\" element={<SettingsPage />} />\n"
content = re.sub(r"(<Route path=\"prompt-improver\" element=\{<PromptImprover />\} />\n)", r"\1" + route_stmt, content)

with open('frontend/src/App.tsx', 'w') as f:
    f.write(content)
