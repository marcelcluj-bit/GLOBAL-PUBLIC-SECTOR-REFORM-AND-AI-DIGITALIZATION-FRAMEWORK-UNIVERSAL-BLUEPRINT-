"""
Public Sector Optimization Engine (Global Framework)
----------------------------------------------------
An open-source simulation module for public sector restructuring,
territorial consolidation, AI workload substitution, and 5-year financial forecasting.

License: MIT / CC0 (Public Domain)
"""

from typing import Dict, List
import dataclasses


@dataclasses.dataclass
class CountryAdministrativeProfile:
    country_name: str
    currency_symbol: str
    total_population: int
    current_public_employees: int
    target_public_employees: int
    avg_annual_public_salary: float
    avg_private_gdp_contribution_per_worker: float
    private_employer_tax_relief_per_worker: float
    it_reinvestment_rate_from_savings: float = 0.15


class PublicSectorOptimizer:
    def __init__(self, profile: CountryAdministrativeProfile):
        self.profile = profile

    def calculate_territorial_consolidation(self, lau_units: List[Dict[str, int]], min_population_threshold: int) -> Dict[str, int]:
        """
        Evaluates Local Administrative Units (LAUs) and calculates required consolidations.
        """
        below_threshold = [u for u in lau_units if u["population"] < min_population_threshold]
        above_threshold = [u for u in lau_units if u["population"] >= min_population_threshold]
        
        total_merged_units = len(below_threshold)
        estimated_new_units = max(1, total_merged_units // 3)
        final_unit_count = len(above_threshold) + estimated_new_units
        
        return {
            "initial_units": len(lau_units),
            "units_below_threshold": total_merged_units,
            "consolidated_final_units": final_unit_count,
            "eliminated_administrative_hubs": len(lau_units) - final_unit_count
        }

    def simulate_5yr_financial_projection(self) -> Dict[str, List[float]]:
        """
        Computes 5-Year Financial Projections (Payroll savings, IT spend, Severance, GDP gain, Net Fiscal Impact).
        """
        total_employees_to_transition = self.profile.current_public_employees - self.profile.target_public_employees
        annual_salary = self.profile.avg_annual_public_salary
        gdp_per_worker = self.profile.avg_private_gdp_contribution_per_worker
        
        # Phase-in execution ratios over 5 years
        downsizing_ratios = [0.15, 0.40, 0.75, 1.00, 1.00]
        
        yearly_payroll_savings: List[float] = []
        yearly_it_investment: List[float] = []
        yearly_severance_costs: List[float] = []
        yearly_gdp_additions: List[float] = []
        yearly_net_budget_impact: List[float] = []

        for yr_idx, ratio in enumerate(downsizing_ratios):
            workers_transitioned = total_employees_to_transition * ratio
            
            # Gross annual payroll savings
            payroll_saving = workers_transitioned * annual_salary
            yearly_payroll_savings.append(round(payroll_saving, 2))
            
            # Mandatory IT & AI reinvestment
            it_invest = payroll_saving * self.profile.it_reinvestment_rate_from_savings
            yearly_it_investment.append(round(it_invest, 2))
            
            # Severance and retraining package allocation (tapering over time)
            if yr_idx < 4:
                newly_transitioned = workers_transitioned if yr_idx == 0 else (workers_transitioned - (total_employees_to_transition * downsizing_ratios[yr_idx - 1]))
                severance = newly_transitioned * (annual_salary * 0.5)
            else:
                severance = 0.0
            yearly_severance_costs.append(round(severance, 2))
            
            # Private sector GDP contribution
            gdp_gain = workers_transitioned * gdp_per_worker
            yearly_gdp_additions.append(round(gdp_gain, 2))
            
            # Net Fiscal Budget Impact = Payroll Savings - IT Invest - Severance
            net_impact = payroll_saving - it_invest - severance
            yearly_net_budget_impact.append(round(net_impact, 2))

        return {
            "yearly_payroll_savings": yearly_payroll_savings,
            "yearly_it_investment": yearly_it_investment,
            "yearly_severance_costs": yearly_severance_costs,
            "yearly_gdp_additions": yearly_gdp_additions,
            "yearly_net_budget_impact": yearly_net_budget_impact
        }

    def print_summary_report(self):
        proj = self.simulate_5yr_financial_projection()
        sym = self.profile.currency_symbol
        
        print("=" * 75)
        print(f" GLOBAL PUBLIC SECTOR OPTIMIZATION SIMULATION: {self.profile.country_name.upper()}")
        print("=" * 75)
        print(f"Total Population:               {self.profile.total_population:,}")
        print(f"Current Public Employees:       {self.profile.current_public_employees:,}")
        print(f"Target Public Employees:        {self.profile.target_public_employees:,}")
        print(f"Personnel to Transition:        {self.profile.current_public_employees - self.profile.target_public_employees:,}")
        print("-" * 75)
        print("FIVE-YEAR FINANCIAL FORECAST (Summary in Currency Units):")
        print(f"{'Year':<6} | {'Payroll Savings':<18} | {'IT Reinvestment':<18} | {'Net Budget Impact':<18}")
        print("-" * 75)
        
        for i in range(5):
            print(f"Year {i+1:<1} | {sym}{proj['yearly_payroll_savings'][i]:>16,.2f} | {sym}{proj['yearly_it_investment'][i]:>16,.2f} | {sym}{proj['yearly_net_budget_impact'][i]:>16,.2f}")
            
        print("-" * 75)
        five_yr_net_sum = sum(proj['yearly_net_budget_impact'])
        five_yr_gdp_sum = sum(proj['yearly_gdp_additions'])
        print(f"5-Year Cumulative Net Budget Benefit:  {sym}{five_yr_net_sum:,.2f}")
        print(f"5-Year Cumulative Private GDP Gain:    {sym}{five_yr_gdp_sum:,.2f}")
        print("=" * 75)


# --------------------------------------------------------------------
# Example Execution: Generic Model State (Scalable to Any Nation)
# --------------------------------------------------------------------
if __name__ == "__main__":
    sample_country = CountryAdministrativeProfile(
        country_name="Generic Sovereign State",
        currency_symbol="$",
        total_population=20_000_000,
        current_public_employees=1_400_000,
        target_public_employees=850_000,
        avg_annual_public_salary=22_000.0,
        avg_private_gdp_contribution_per_worker=35_000.0,
        private_employer_tax_relief_per_worker=5_000.0,
        it_reinvestment_rate_from_savings=0.15
    )

    optimizer = PublicSectorOptimizer(sample_country)
    optimizer.print_summary_report()
