import graphviz
from graphviz import Digraph

def create_privilege_dfa():
    """
    Creates a DFA for detecting high-privileged system commands
    Focuses on commands like sudo, chmod, rm -rf, useradd, etc.
    Optimized for horizontal landscape layout.
    """
    
    # Create a new directed graph
    dot = Digraph(comment='Privileged Command Detection DFA')
    
    # Set graph attributes for horizontal landscape layout
    dot.attr(rankdir='LR', size='28,18', dpi='300')
    dot.attr('node', shape='circle', style='filled', fontname='Arial Bold', fontsize='9')
    dot.attr('edge', fontname='Arial', fontsize='7', arrowsize='0.6')
    dot.attr(concentrate='false', splines='curved', nodesep='0.6', ranksep='2.0')
    dot.attr(bgcolor='white')
    
    # Define color scheme for different privilege levels
    colors = {
        'start': '#E3F2FD',
        'scan': '#BBDEFB',
        'sudo': '#FFCDD2',
        'file': '#E1BEE7',
        'destructive': '#FF8A65', 
        'user': '#C8E6C9',
        'system': '#90CAF9',
        'accept': '#66BB6A',
        'risk': '#F44336',
        'clean': '#81C784',
        'report': '#FFB74D'
    }
    
    # Add nodes with colors and labels
    
    # Start and main states
    dot.node('START', 'START', fillcolor=colors['start'], shape='point', width='0.3')
    dot.node('SCAN', 'SCAN', fillcolor=colors['scan'], fontsize='11')
    
    # Sudo command pattern
    dot.node('SUDO_S', 'S', fillcolor=colors['sudo'])
    dot.node('SUDO_U', 'U', fillcolor=colors['sudo'])
    dot.node('SUDO_D', 'D', fillcolor=colors['sudo'])
    dot.node('SUDO_O', 'O', fillcolor=colors['sudo'])
    
    # Chmod command pattern
    dot.node('CHMOD_C', 'C', fillcolor=colors['file'])
    dot.node('CHMOD_H', 'H', fillcolor=colors['file'])
    dot.node('CHMOD_M', 'M', fillcolor=colors['file'])
    dot.node('CHMOD_O', 'O', fillcolor=colors['file'])
    dot.node('CHMOD_D', 'D', fillcolor=colors['file'])
    dot.node('CHMOD_PERM', 'PERM', fillcolor=colors['file'])
    
    # Rm -rf command pattern
    dot.node('RM_R', 'R', fillcolor=colors['destructive'])
    dot.node('RM_M', 'M', fillcolor=colors['destructive'])
    dot.node('RM_DASH', '-', fillcolor=colors['destructive'])
    dot.node('RM_RF', 'RF', fillcolor=colors['destructive'])
    
    # User management pattern
    dot.node('USER_U', 'U', fillcolor=colors['user'])
    dot.node('USER_S', 'S', fillcolor=colors['user'])
    dot.node('USER_E', 'E', fillcolor=colors['user'])
    dot.node('USER_R', 'R', fillcolor=colors['user'])
    dot.node('USER_A', 'A', fillcolor=colors['user'])
    dot.node('USER_D', 'D', fillcolor=colors['user'])
    dot.node('USER_DD', 'D', fillcolor=colors['user'])
    
    # System control pattern
    dot.node('SYS_S', 'S', fillcolor=colors['system'])
    dot.node('SYS_Y', 'Y', fillcolor=colors['system'])
    dot.node('SYS_S2', 'S', fillcolor=colors['system'])
    dot.node('SYS_T', 'T', fillcolor=colors['system'])
    dot.node('SYS_E', 'E', fillcolor=colors['system'])
    dot.node('SYS_M', 'M', fillcolor=colors['system'])
    dot.node('SYS_C', 'C', fillcolor=colors['system'])
    dot.node('SYS_T2', 'T', fillcolor=colors['system'])
    dot.node('SYS_L', 'L', fillcolor=colors['system'])
    
    # Accept states
    dot.node('SUDO_ACCEPT', 'SUDO\\nDETECTED', fillcolor=colors['accept'], shape='doublecircle', fontsize='8')
    dot.node('CHMOD_ACCEPT', 'CHMOD\\nDETECTED', fillcolor=colors['accept'], shape='doublecircle', fontsize='8')
    dot.node('RM_ACCEPT', 'RM -RF\\nDETECTED', fillcolor=colors['accept'], shape='doublecircle', fontsize='8')
    dot.node('USER_ACCEPT', 'USERADD\\nDETECTED', fillcolor=colors['accept'], shape='doublecircle', fontsize='8')
    dot.node('SYS_ACCEPT', 'SYSTEMCTL\\nDETECTED', fillcolor=colors['accept'], shape='doublecircle', fontsize='8')
    
    # Risk levels
    dot.node('RISK_LEVEL_1', 'LOW\\nRISK', fillcolor=colors['risk'], shape='doublecircle', fontcolor='white', fontsize='8')
    dot.node('RISK_LEVEL_2', 'MED\\nRISK', fillcolor=colors['risk'], shape='doublecircle', fontcolor='white', fontsize='8')
    dot.node('RISK_LEVEL_3', 'HIGH\\nRISK', fillcolor=colors['risk'], shape='doublecircle', fontcolor='white', fontsize='8')
    
    # Clean and report states
    dot.node('CLEAN', 'CLEAN', fillcolor=colors['clean'], shape='doublecircle', fontcolor='white')
    dot.node('REPORT', 'REPORT', fillcolor=colors['report'], shape='doublecircle', fontcolor='white', fontsize='10')
    
    # Use invisible nodes to control layout
    dot.node('inv1', style='invis')
    dot.node('inv2', style='invis')
    dot.node('inv3', style='invis')
    
    # Add edges
    
    # Initial transition
    dot.edge('START', 'SCAN', label='input')
    
    # Sudo command pattern
    dot.edge('SCAN', 'SUDO_S', label="'s'", color='#FF5252')
    dot.edge('SUDO_S', 'SUDO_U', label="'u'", color='#FF5252')
    dot.edge('SUDO_U', 'SUDO_D', label="'d'", color='#FF5252')
    dot.edge('SUDO_D', 'SUDO_O', label="'o'", color='#FF5252')
    dot.edge('SUDO_O', 'SUDO_ACCEPT', label="space", color='#FF5252', penwidth='2')
    
    # Chmod command pattern
    dot.edge('SCAN', 'CHMOD_C', label="'c'", color='#7E57C2')
    dot.edge('CHMOD_C', 'CHMOD_H', label="'h'", color='#7E57C2')
    dot.edge('CHMOD_H', 'CHMOD_M', label="'m'", color='#7E57C2')
    dot.edge('CHMOD_M', 'CHMOD_O', label="'o'", color='#7E57C2')
    dot.edge('CHMOD_O', 'CHMOD_D', label="'d'", color='#7E57C2')
    dot.edge('CHMOD_D', 'CHMOD_PERM', label="space + [0-7]{3}", color='#7E57C2', penwidth='2')
    dot.edge('CHMOD_PERM', 'CHMOD_ACCEPT', color='#7E57C2', penwidth='2')
    
    # Rm -rf command pattern
    dot.edge('SCAN', 'RM_R', label="'r'", color='#FF7043')
    dot.edge('RM_R', 'RM_M', label="'m'", color='#FF7043')
    dot.edge('RM_M', 'RM_DASH', label="space + '-'", color='#FF7043')
    dot.edge('RM_DASH', 'RM_RF', label="'r'", color='#FF7043')
    dot.edge('RM_RF', 'RM_ACCEPT', label="'f'", color='#FF7043', penwidth='2')
    
    # User management pattern
    dot.edge('SCAN', 'USER_U', label="'u'", color='#66BB6A')
    dot.edge('USER_U', 'USER_S', label="'s'", color='#66BB6A')
    dot.edge('USER_S', 'USER_E', label="'e'", color='#66BB6A')
    dot.edge('USER_E', 'USER_R', label="'r'", color='#66BB6A')
    dot.edge('USER_R', 'USER_A', label="'a'", color='#66BB6A')
    dot.edge('USER_A', 'USER_D', label="'d'", color='#66BB6A')
    dot.edge('USER_D', 'USER_DD', label="'d'", color='#66BB6A')
    dot.edge('USER_DD', 'USER_ACCEPT', color='#66BB6A', penwidth='2')
    
    # System control pattern
    dot.edge('SCAN', 'SYS_S', label="'s'", color='#42A5F5')
    dot.edge('SYS_S', 'SYS_Y', label="'y'", color='#42A5F5')
    dot.edge('SYS_Y', 'SYS_S2', label="'s'", color='#42A5F5')
    dot.edge('SYS_S2', 'SYS_T', label="'t'", color='#42A5F5')
    dot.edge('SYS_T', 'SYS_E', label="'e'", color='#42A5F5')
    dot.edge('SYS_E', 'SYS_M', label="'m'", color='#42A5F5')
    dot.edge('SYS_M', 'SYS_C', label="'c'", color='#42A5F5')
    dot.edge('SYS_C', 'SYS_T2', label="'t'", color='#42A5F5')
    dot.edge('SYS_T2', 'SYS_L', label="'l'", color='#42A5F5')
    dot.edge('SYS_L', 'SYS_ACCEPT', label="space + (start|stop|restart)", color='#42A5F5', penwidth='2')
    
    # Accept to risk level transitions
    dot.edge('USER_ACCEPT', 'RISK_LEVEL_1', label='User\\nMgmt', color='#66BB6A', penwidth='2')
    dot.edge('SYS_ACCEPT', 'RISK_LEVEL_1', label='System\\nCtrl', color='#42A5F5', penwidth='2')
    dot.edge('SUDO_ACCEPT', 'RISK_LEVEL_2', label='Priv\\nEsc', color='#FF5252', penwidth='2')
    dot.edge('CHMOD_ACCEPT', 'RISK_LEVEL_2', label='File\\nPerm', color='#7E57C2', penwidth='2')
    dot.edge('RM_ACCEPT', 'RISK_LEVEL_3', label='Destructive\\nCmd', color='#FF7043', penwidth='2')
    
    # Risk levels to report
    dot.edge('RISK_LEVEL_1', 'REPORT', label='Low', color='#66BB6A')
    dot.edge('RISK_LEVEL_2', 'REPORT', label='Med', color='#FFA000')
    dot.edge('RISK_LEVEL_3', 'REPORT', label='High', color='#F44336')
    
    # Continue scanning transitions
    dot.edge('SUDO_ACCEPT', 'SCAN', label='continue', style='dashed', color='gray')
    dot.edge('CHMOD_ACCEPT', 'SCAN', label='continue', style='dashed', color='gray')  
    dot.edge('RM_ACCEPT', 'SCAN', label='continue', style='dashed', color='gray')
    dot.edge('USER_ACCEPT', 'SCAN', label='continue', style='dashed', color='gray')
    dot.edge('SYS_ACCEPT', 'SCAN', label='continue', style='dashed', color='gray')
    
    # Key reject transitions (showing main failure paths)
    dot.edge('SUDO_S', 'SCAN', label='other', color='lightgray', style='dashed') 
    dot.edge('CHMOD_C', 'SCAN', label='other', color='lightgray', style='dashed')
    dot.edge('RM_R', 'SCAN', label='other', color='lightgray', style='dashed')
    dot.edge('USER_U', 'SCAN', label='other', color='lightgray', style='dashed')
    dot.edge('SYS_S', 'SCAN', label='other', color='lightgray', style='dashed')
    
    # Default and EOF transitions
    dot.edge('SCAN', 'SCAN', label='default', style='dotted', color='blue')
    dot.edge('SCAN', 'CLEAN', label='EOF', color='green')
    dot.edge('CLEAN', 'REPORT', label='safe', color='green')
    
    # Layout constraints using invisible edges
    dot.edge('START', 'inv1', style='invis')
    dot.edge('inv1', 'SUDO_ACCEPT', style='invis')
    dot.edge('inv1', 'CHMOD_ACCEPT', style='invis')
    dot.edge('inv1', 'RM_ACCEPT', style='invis')
    dot.edge('inv1', 'USER_ACCEPT', style='invis')
    dot.edge('inv1', 'SYS_ACCEPT', style='invis')
    
    return dot

def main():
    """Generate the DFA and save as SVG"""
    
    # Create the DFA
    dfa = create_privilege_dfa()
    
    # Save as SVG
    try:
        dfa.render('privilege_command_dfa', format='svg', cleanup=True)
        print("✅ Privilege Command DFA successfully generated as 'privilege_command_dfa.svg'")
        print("🎨 Optimized features:")
        print("   • Focuses on privileged command detection (sudo, chmod, rm -rf, etc.)")
        print("   • Color-coded by command category")
        print("   • Risk level mapping (Low, Med, High)")
        print("   • Clean horizontal layout")
        print("   • Professional design suitable for academic presentations")
        
    except Exception as e:
        print(f"❌ Error generating SVG: {e}")
        print("💡 Make sure you have graphviz installed:")
        print("   pip install graphviz")
        print("   And the graphviz system package:")
        print("   - Ubuntu/Debian: sudo apt-get install graphviz")
        print("   - macOS: brew install graphviz")
        print("   - Windows: Download from https://graphviz.org/download/")

if __name__ == "__main__":
    main()