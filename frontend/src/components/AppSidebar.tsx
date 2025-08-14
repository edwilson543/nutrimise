import { NavLink, useLocation } from "react-router-dom";
import { UtensilsCrossed, CalendarDays, Apple } from "lucide-react";
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarTrigger,
  useSidebar,
  SidebarHeader,
  SidebarFooter,
} from "@/components/ui/sidebar";

const items = [
  { title: "Recipes", url: "/recipes", icon: UtensilsCrossed },
  { title: "Plans", url: "/plans", icon: CalendarDays },
  { title: "Nutrition", url: "/nutrition", icon: Apple },
];

export function AppSidebar() {
  const { state } = useSidebar();
  const location = useLocation();
  const currentPath = location.pathname;

  const isActive = (path: string) => currentPath === path;
  const getNavCls = ({ isActive }: { isActive: boolean }) =>
    isActive ? "bg-sidebar-accent text-sidebar-accent-foreground font-medium" : "hover:bg-sidebar-accent hover:text-sidebar-accent-foreground";

  return (
    <Sidebar className={state === "collapsed" ? "w-14" : "w-64"} collapsible="offcanvas">
      <SidebarHeader>
        <div className="flex items-center justify-between px-2 py-1">
          <div className="flex items-center gap-2">
            <div className="h-7 w-7 rounded-md" style={{ backgroundImage: "var(--gradient-primary)" }} />
            <span className="text-sm font-semibold tracking-wide">NutriMise</span>
          </div>
          <SidebarTrigger className="self-end" />
        </div>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Navigate</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {items.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton asChild isActive={isActive(item.url)}>
                    <NavLink to={item.url} end className={getNavCls}>
                      <item.icon className="mr-2 h-4 w-4" />
                      <span>{item.title}</span>
                    </NavLink>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter>
        <p className="text-xs text-muted-foreground px-2">Eat better, feel better.</p>
      </SidebarFooter>
    </Sidebar>
  );
}
